"""Audit recipe metadata without asserting photo rights or visual correspondence.

Run: python scripts/audit_recipes.py
"""
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def load_recipes():
    source=(ROOT/"assets/data.js").read_text(encoding="utf-8")
    data=json.loads(re.sub(r";\s*$","",re.sub(r"^window\.DANTAS_DATA\s*=\s*","",source)))
    return data["recipes"]


def inspect_recipe(recipe):
    issues=[]
    if not recipe.get("image"):
        issues.append("imagem ausente")
    if not recipe.get("imageCredit"):
        issues.append("crédito da imagem não documentado")
    if not recipe.get("source"):
        issues.append("origem editorial ausente")
    if not recipe.get("sourceUrl"):
        issues.append("URL da referência não documentada (pode ser receita própria)")
    if not recipe.get("steps"):
        issues.append("preparo ausente")
    if not recipe.get("servings") or recipe["servings"]<=0:
        issues.append("rendimento inválido")
    for i, ingredient in enumerate(recipe.get("ingredients",[]),1):
        if not isinstance(ingredient,dict) or not all(ingredient.get(k) for k in ("quantity","unit","name")):
            issues.append(f"ingrediente {i} incompleto")
    return issues


def report():
    recipes=load_recipes()
    lines=["# Auditoria editorial das receitas","","Relatório gerado a partir dos metadados locais. Não comprova direitos de imagem, correspondência visual, validade dos links ou testes culinários.","",f"Total de receitas: **{len(recipes)}**.","","| Receita | Pendências de metadados |","|---|---|"]
    for r in recipes:
        issues=inspect_recipe(r)
        title=r["title"].replace("|","/")
        lines.append(f"| {title} | {'; '.join(issues) if issues else 'Sem pendências detectadas automaticamente'} |")
    lines+=["","## Revisão humana obrigatória","",
            "- Abrir cada imagem e verificar se representa o prato ou é apenas uma ilustração aceitável.",
            "- Confirmar titularidade, licença, permissão e atribuição da fotografia; substituir imagens sem direitos claros.",
            "- Verificar que o link da fonte existe e corresponde ao conteúdo citado.",
            "- Revisar medidas, tempo, segurança alimentar e etapas com especialista; o script não valida precisão culinária.",
            "- Para receitas autorais sem URL externa, registrar a origem de modo explícito; não inventar referência."]
    return "\n".join(lines)+"\n"


if __name__=="__main__":
    print(report())
