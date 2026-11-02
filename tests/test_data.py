import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from weekly_update import load,update,week_id,save

class ContentTests(unittest.TestCase):
  def test_content_schema_and_unique_ids(self):
    d=load(BASE/'assets'/'data.js')
    self.assertGreaterEqual(len(d['recipes']),15)
    self.assertEqual(len({r['id'] for r in d['recipes']}),len(d['recipes']))
    self.assertEqual(len({t['id'] for t in d['techniques']}),len(d['techniques']))
    editorial=[r for r in d['recipes'] if r.get('curationStatus')=='fonte-editorial-verificada' and r.get('sourceUrl')]
    self.assertEqual(len({r['sourceUrl'] for r in editorial}),len(editorial))
    self.assertTrue(all(r.get('sourceName') and r.get('sourceUrl','').startswith('https://') for r in d['recipes'] if r.get('curationStatus')=='fonte-editorial-verificada'))
    self.assertTrue(all(v['url'].startswith('https://') and 'results?search_query=' not in v['url'] for v in d['videos']))
    self.assertTrue(all(w.get('eventDate','9999-12-31')>='2026-10-26' for w in d['workshops'] if w.get('verifiedAt')=='2026-10-26'))
    self.assertGreaterEqual(len(d['workshops']),3)
    self.assertTrue(all(w['url'].startswith('https://') for w in d['workshops']))
    for r in d['recipes']+[q for q in d['curatedQueue'] if 'ingredients' in q]:
      self.assertIn(r['category'],('entrada','principal','sobremesa'))
      self.assertGreaterEqual(len(r['steps']),3)
      self.assertTrue(r['ingredients'] or (r.get('sourceUrl','').startswith('https://') and r.get('sourceName')))
      self.assertTrue(all((isinstance(i,str) and bool(i.strip())) or (isinstance(i,dict) and i.get('quantity',0)>0 and i.get('unit') and i.get('name')) for i in r['ingredients']))
      self.assertGreater(r['servings'],0)
  def test_all_published_recipes_are_complete(self):
    d=load(BASE/'assets'/'data.js')
    for r in d['recipes']:
      with self.subTest(recipe=r['id']):
        self.assertTrue(r['ingredients'], 'Receita sem ingredientes ou quantidades')
        self.assertTrue(all(isinstance(i,dict) and i.get('quantity',0)>0 and i.get('unit') and i.get('name') for i in r['ingredients']))
        self.assertGreaterEqual(len(r['steps']),3)
        self.assertFalse(any('consulte a fonte' in step.lower() or 'confira os ingredientes' in step.lower() for step in r['steps']))
    for lesson in d['techniques']:
      with self.subTest(lesson=lesson['id']):
        self.assertGreaterEqual(len(lesson.get('lesson',[])),2)
        self.assertTrue(lesson.get('mistakes'))

  def test_verified_editorial_selections_and_upcoming_workshops(self):
    d=load(BASE/'assets'/'data.js')
    published_urls={r.get('sourceUrl') for r in d['recipes'] if r.get('sourceUrl')}
    selected=d.get('curatedDiscoveries',[])
    self.assertGreaterEqual(len(selected),3)
    self.assertEqual(len({r['id'] for r in selected}),len(selected))
    self.assertEqual(len({r['sourceUrl'] for r in selected}),len(selected))
    for r in selected:
      with self.subTest(selection=r['id']):
        self.assertNotIn(r['sourceUrl'],published_urls,'Fonte duplicada no catálogo')
        self.assertTrue(r['sourceUrl'].startswith('https://'))
        self.assertTrue(r.get('author') and r.get('sourceName'))
        self.assertTrue(r.get('description') and len(r.get('mainIngredients',[]))>=3)
        self.assertEqual(r.get('curationStatus'),'fonte-editorial-verificada')
        self.assertNotIn('steps',r,'Curadoria não deve copiar modo de preparo')
        self.assertNotIn('ingredients',r,'Curadoria não deve inventar quantidades')
        self.assertNotIn('tested',r,'Curadoria não deve alegar teste')
    self.assertEqual(len({w['url'] for w in d['workshops']}),len(d['workshops']))
    for w in d['workshops']:
      if w.get('eventDate'):
        self.assertGreaterEqual(w['eventDate'],'2026-11-02','Não publicar oficina expirada')
        self.assertTrue(w.get('verifiedAt'))

  def test_weekly_publishes_recipe_and_technique_once(self):
    d=load(BASE/'assets'/'data.js')
    with tempfile.TemporaryDirectory() as tmp:
      path=Path(tmp)/'data.js';save(path,d)
      dt=datetime(2026,10,19,tzinfo=ZoneInfo('America/Sao_Paulo'))
      self.assertFalse(update(path,dt))
      after=load(path)
      self.assertEqual(len(after['recipes']),len(d['recipes']))
      self.assertEqual(len(after['techniques']),len(d['techniques']))
      self.assertFalse(update(path,dt))
      self.assertEqual(len(load(path)['recipes']),len(after['recipes']))
  def test_week_id_year_boundaries(self):
    a=datetime(2026,12,31,tzinfo=ZoneInfo('America/Sao_Paulo'))
    b=datetime(2027,1,1,tzinfo=ZoneInfo('America/Sao_Paulo'))
    self.assertEqual(week_id(a),week_id(b))

if __name__=='__main__':unittest.main()
