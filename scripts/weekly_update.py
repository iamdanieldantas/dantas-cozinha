#!/usr/bin/env python3
"""Publish up to one original recipe + one technique per ISO week.

With OPENAI_API_KEY, new original content is generated using a model.
Without a key, the finite curated queue is used. Workshop dates are never generated.
No external dependencies: Python 3.11+ only.
"""
import argparse
from datetime import datetime, date
from zoneinfo import ZoneInfo
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONTENT_FILE = ROOT / 'assets' / 'data.js'
PREFIX = 'window.DANTAS_DATA = '


def load(path):
    text = path.read_text(encoding='utf-8').strip()
    if not text.startswith(PREFIX) or not text.endswith(';'):
        raise ValueError('Arquivo de dados inesperado')
    return json.loads(text[len(PREFIX):-1])


def save(path, data):
    path.write_text(PREFIX + json.dumps(data, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')


def week_id(now):
    iso = now.isocalendar()
    return f'{iso.year}-W{iso.week:02d}'


def slug(text):
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:48]
    return (s or 'conteudo') + '-' + hashlib.sha256(text.encode()).hexdigest()[:6]


def ai_generate(data, today):
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        return None
    titles = [r['title'] for r in data['recipes']][-40:]
    schema = {
       'type': 'object', 'additionalProperties': False,
       'properties': {
         'recipe': {'type': 'object', 'additionalProperties': False,
           'properties': {
             'title': {'type':'string'}, 'category': {'type':'string','enum':['entrada','principal','sobremesa']},
             'description': {'type':'string'},'minutes': {'type':'integer'}, 'difficulty': {'type':'string','enum':['Fácil','Intermediário']},
             'servings': {'type':'integer'}, 'ingredients': {'type':'array','items': {'type':'object','additionalProperties':False,
                'properties':{'name':{'type':'string'},'quantity':{'type':'number'},'unit':{'type':'string'}}, 'required':['name','quantity','unit']}},
             'steps': {'type':'array','items':{'type':'string'}},'tip': {'type':'string'}, 'tags': {'type':'array','items':{'type':'string'}}
           },'required':['title','category','description','minutes','difficulty','servings','ingredients','steps','tip','tags']},
         'technique': {'type':'object','additionalProperties':False,
           'properties': {'title': {'type':'string'}, 'category': {'type':'string'}, 'summary': {'type':'string'},
             'why': {'type':'string'}, 'practice': {'type':'string'}},
           'required':['title','category','summary','why','practice']}
       }, 'required':['recipe','technique']
    }
    prompt=(f'Data: {today}. Você é um editor culinário brasileiro rigoroso. Gere exatamente UMA receita original '
      'e UM estudo curto de técnicas culinárias em português do Brasil. Priorizamos culinária caseira, sobremesas, '
      'entradas e pratos principais. Diversifique as categorias e evite estas receitas já existentes: '
      + '; '.join(titles)
      + '. Forneça ingredientes com quantidades plausíveis e unidade precisa, e etapas completas coerentes com o tempo/porções. '
      'Evite dicas perigosas de segurança alimentar; aves totalmente cozidas, ingredientes conservados adequadamente. '
      'Não invente fatos históricos, benefícios à saúde, estudos científicos, citações, preços, eventos, datas, '
      'Instagram, disponibilidade, perfis ou links. Sem instruções de preparar carnes cruas para consumo. '
      'A receita deve ser prática em cozinha doméstica e o texto revisável, original e direto.')
    body = {
      'model': os.getenv('OPENAI_MODEL','gpt-4.1-mini'),
      'instructions': 'Retorne somente os dados pedidos, seguindo o esquema JSON. Não cite fontes inventadas.',
      'input': prompt,
      'text': {'format':{'type':'json_schema','name':'conteudo_culinaria','strict':True,'schema':schema}},
      'max_output_tokens': 2800,
    }
    req = Request('https://api.openai.com/v1/responses',
                  data=json.dumps(body).encode('utf-8'),
                  headers={'Authorization': 'Bearer '+key,'Content-Type':'application/json'},
                  method='POST')
    with urlopen(req,timeout=75) as response:
        raw=json.load(response)
    parts=[c.get('text','') for output in raw.get('output',[]) for c in output.get('content',[]) if c.get('type')=='output_text']
    if not parts: raise ValueError('API não retornou texto para publicação')
    generated=json.loads(''.join(parts))
    r,t=generated['recipe'],generated['technique']
    for field in ('title','description','tip'):
        if not (4<=len(r[field].strip())<=500):raise ValueError('Campo de receita inválido '+field)
    if not (1<=r['minutes']<=600 and 1<=r['servings']<=20 and 3<=len(r['steps'])<=15 and 3<=len(r['ingredients'])<=25):
        raise ValueError('Receita incoerente: tempo, porções ou etapas')
    if any(i['quantity']<=0 or i['quantity']>20000 or not i['unit'].strip() or not i['name'].strip() for i in r['ingredients']):
        raise ValueError('Ingrediente com quantidade/unidade inválida')
    if any(r['title'].casefold()==prev['title'].casefold() for prev in data['recipes']):
        raise ValueError('Título da receita duplicado')
    if any(t['title'].casefold()==prev['title'].casefold() for prev in data['techniques']):
        raise ValueError('Título do estudo duplicado')
    photos={
       'entrada':'photo-1512621776951-a57141f2eefd',
       'principal':'photo-1473093295043-cdd812d0e601',
       'sobremesa':'photo-1488477181946-6428a0291777'
    }
    r.update({'id':'ai-'+slug(r['title']), 'emoji': {'entrada':'🥗','principal':'🍝','sobremesa':'🍰'}[r['category']],
             'image':'https://images.unsplash.com/'+photos[r['category']]+'?auto=format&fit=crop&w=940&q=80',
             'createdAt':today,'source':'Receita produzida automaticamente por IA; recomenda-se revisão antes de cozinhar'})
    t.update({'id':'ai-'+slug(t['title']),'createdAt':today})
    return r,t


def release_curated(data):
    queue=data.get('curatedQueue',[])
    recipes=[x for x in queue if 'ingredients' in x and 'steps' in x]
    techniques=[x for x in queue if 'summary' in x and 'why' in x]
    published=[]
    if recipes:
        item=recipes[0]
        data['recipes'].append(item)
        queue.remove(item)
        published.append('receita')
    if techniques:
        item=techniques[0]
        data['techniques'].append(item)
        queue.remove(item)
        published.append('técnica')
    return published


def update(path, now, api_func=ai_generate):
    data=load(path)
    wid=week_id(now)
    if any(item.get('week')==wid for item in data.get('releaseHistory',[])):
        print(f'{wid}: conteúdo já publicado. Nenhuma alteração.')
        return False
    today=now.date().isoformat()
    new_content=None
    if os.getenv('OPENAI_API_KEY'):
        try: new_content=api_func(data,today)
        except Exception as e: print('Falha na geração por API: '+str(e),file=sys.stderr)
    if new_content:
        r,t=new_content
        data['recipes'].append(r)
        data['techniques'].append(t)
        published=['receita gerada por IA','técnica gerada por IA']
    else:
        published=release_curated(data)
    if not published:
        print(f'{wid}: sem conteúdo para publicar. Configure OPENAI_API_KEY ou amplie a fila editorial.')
        return False
    data['generatedAt']=now.isoformat()
    data.setdefault('releaseHistory',[]).append({'week':wid,'date':today,'published':published})
    save(path,data)
    print(f'{wid}: publicado: {", ".join(published)}')
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Atualizador semanal Dantas Cozinha')
    p.add_argument('--path',type=Path,default=CONTENT_FILE)
    p.add_argument('--date',type=str,help='Data local ISO (teste), p.ex. 2026-10-19')
    args=p.parse_args()
    if args.date: now=datetime.combine(date.fromisoformat(args.date),datetime.min.time(),tzinfo=ZoneInfo('America/Sao_Paulo'))
    else: now=datetime.now(ZoneInfo('America/Sao_Paulo'))
    update(args.path,now)
