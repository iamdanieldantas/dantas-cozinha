---
name: content-standards
description: Padronizar receitas, aulas, oficinas, vídeos e curadoria do Dantas Cozinha antes de publicar.
---

# Skill: padrões de conteúdo

Fonte canônica: assets/data.js (window.DANTAS_DATA). Não executar seed_content.py para atualizar o catálogo: ele recria os dados.

## Tipos e contratos

- recipes: id, title, category, description, minutes, difficulty, servings, image, ingredients, steps, tip, createdAt, source. category: entrada, principal ou sobremesa. ingredients: objetos com quantity positiva, unit e name; steps: etapas detalhadas ordenadas. Exibir porções, quantidades, ingredientes e preparo integral do próprio portal.
- techniques: id, title, category, summary, why, practice, createdAt, lesson, mistakes, deepDive. lesson é lista de seções heading/body, com conteúdo suficiente para expansão. Sempre incluir erros comuns e prática.
- workshops: id, name, neighborhood, address, description, url, tag, verifiedAt; eventDate pode ser uma data ISO ou null. Aulas passadas podem permanecer no histórico e não aparecer no site. Nunca inventar vagas, datas ou preços.
- videos: id, title, topic, description, url, platform, verifiedAt. Fonte oficial identificada.
- curatedDiscoveries: id, title, category, description, mainIngredients, author, sourceName, sourceUrl, verifiedAt, createdAt, curationStatus. É ficha editorial resumida, não receita completa: não inventar quantidades ou preparo, preservar o link para a fonte original.

## Regras gerais

1. Identificadores estáveis e únicos. Títulos não duplicados dentro do tipo. URLs de curadoria únicas.
2. Datas ISO válidas e URLs externas HTTPS. Nunca inventar autor, teste, fonte, imagem, data, preço, vaga ou link.
3. Respeitar direitos autorais: descrever com palavras próprias e atribuir. Receitas de terceiros sem autorização ficam em curatedDiscoveries, sem reprodução integral.
4. Não afirmar testes culinários não realizados. Não inventar segurança alimentar, temperaturas ou benefícios para saúde.
5. Imagens devem ter URL válida, fallback e correspondência com o prato (verificação visual humana).
6. Seguir a política curationPolicy.version >= 2: não reativar gerador legado de receitas fictícias.
7. Antes de qualquer publicação, rodar harness de QA e abrir PR. Nunca escrever diretamente na branch main ou fazer merge automático.

## Fluxo

Planejar → padronizar → validar esquema → testar navegação → auditar fonte e direitos → PR com evidências → revisão humana → merge manual.
