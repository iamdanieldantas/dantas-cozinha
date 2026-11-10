# Dados editoriais modulares

A aplicação continua consumindo `window.DANTAS_DATA` de `assets/data.js` sem alterações na interface, nas URLs ou no `localStorage`.

## Fontes de verdade
- `content/site.json`: identidade e metadados do acervo.
- `content/recipes.json`: receitas.
- `content/school.json`: artigos da Escola.
- `content/discovery.json`: workshops e vídeos.
- `content/curation.json`: política, histórico e descobertas.

## Fluxo editorial
1. Edite somente os arquivos JSON em `content/` para mudanças de conteúdo.
2. Execute `python scripts/build_dataset.py` para atualizar o artefato `assets/data.js`.
3. Execute `python scripts/build_dataset.py --check` e `python -m harness.runner --mode review`.
4. Faça PR e aguarde aprovação explícita no chat antes do merge.

O harness bloqueia divergências **semânticas** entre os arquivos fonte e o artefato gerado. Diferenças apenas de formatação não são consideradas divergência.

**Atenção:** automações e agentes de curadoria que antes alteravam `assets/data.js` diretamente precisam migrar para `content/*.json`, seguidos da geração do arquivo JS. Não editar somente o artefato gerado.

## Rollback
Reverter o PR restaura o modelo anterior de arquivo único. A API do navegador e a estrutura do armazenamento local permanecem inalteradas.
