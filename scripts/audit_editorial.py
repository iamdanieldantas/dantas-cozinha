"""Non-destructive editorial audit: actionable recipe and lesson inventory."""
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
recipes=json.loads((ROOT/"content/recipes.json").read_text(encoding="utf-8"))["recipes"]
lessons=json.loads((ROOT/"content/school.json").read_text(encoding="utf-8"))["techniques"]
issues=[]
images=Counter(r.get("image","") for r in recipes if r.get("image"))
for r in recipes:
    name=r.get("title",r.get("id","?"))
    if not r.get("sourceUrl"):issues.append((r["id"],"missing-source",name))
    if not r.get("imageCredit"):issues.append((r["id"],"image-credit-review",name))
    if not r.get("image"):issues.append((r["id"],"missing-image",name))
    if images[r.get("image","")]>1:issues.append((r["id"],"shared-image-review",name))
    if not r.get("verifiedTestClaim"):issues.append((r["id"],"test-status-review",name))
    if any(term in r.get("description","").lower() for term in ("quantidades e o preparo exatos no site original","medidas e modo de preparo ficam")):
        issues.append((r["id"],"description-conflicts-with-local-recipe",name))
    if not r.get("ingredients") or not r.get("steps"):issues.append((r["id"],"incomplete-recipe",name))
lines=["# Auditoria editorial automatizada — Dantas Cozinha","","Este inventário identifica itens para **revisão humana**. Não comprova direitos de imagem, correspondência fotográfica, segurança alimentar ou teste real de receita.","",f"- Receitas: {len(recipes)}",f"- Aulas: {len(lessons)}",f"- Ocorrências de revisão: {len(issues)}","","| Receita | Revisão necessária |","|---|---|"]
for id,kind,name in issues:
    lines.append(f"| {name.replace('|','/')} (`{id}`) | {kind} |")
lines+=["","## Revisão manual obrigatória","","- Conferir visualmente imagem versus prato e licença de uso, substituindo imagens sem autorização.","- Conferir quantidades, rendimento, preparo, alergênicos e segurança alimentar com responsável editorial.","- Verificar links de origem, autoria e direitos de reprodução; manter créditos.","- Revisar cada aula, especialmente alegações técnicas, atividades e sequência pedagógica.","- Validar desktop/mobile com usuários reais e auditoria Lighthouse no site publicado."]
out=ROOT/"docs/auditoria-editorial-pendente.md"
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Audit written: {len(issues)} issues")
