# Automação do Dantas Cozinha — skills, agentes e harness

Objetivo: corrigir falhas recorrentes do pipeline, padronizar TODOS os conteúdos e automatizar etapas sem perder controle editorial.

## Arquitetura

1. **Skills** em .agents/skills: padrão de conteúdo, quality gates e aprovação de publicação.
2. **Agents** em agents/: editorial-reviewer (IA opcional), qa-agent (determinístico) e publisher-agent (CI/deploy).
3. **Harness** em harness/: valida conteúdo, executa testes com timeout e registra relatório por etapa.
4. **Integração:** GitHub Actions para PRs, artifacts e Pages. MCP pode ser adicionado depois, mas não é necessário para conectar o GitHub.
5. **Aprovação:** todo conteúdo gerado automaticamente vira PR de revisão; não existe auto-merge.

## Comandos locais

Para validar campos de receitas, aulas, oficinas, vídeos e curadoria:

    python -m harness.validate_content

Para executar o harness sem navegador (rápido):

    python -m harness.runner --mode review

Para executar também Playwright (precisa instalar playwright e Chromium):

    python -m harness.runner --mode review --browser

O log de etapas fica em _reports/harness-report.json e deve mostrar duração, status, saída de erros e SHA. O CI faz upload do relatório mesmo quando há falha.

## Agent 1: Auditoria editorial automática

Workflow: Actions > Agent — Auditoria editorial > Run workflow.

- Escopos: all, recipes, techniques, workshops, videos, curatedDiscoveries.
- Roda validação e testes; gera relatório editorial.
- Sem OPENAI_API_KEY: só validações determinísticas e status skipped_no_key.
- Com OPENAI_API_KEY (GitHub Secrets): revisão por modelo de um subconjunto do catálogo, com sugestões para um humano analisar.
- Relatório no artifact agent-editorial-report; não altera nenhum arquivo nem publica.
- Agenda semanal, independente da publicação do site.

## Agent 2: Propor melhoria com IA (múltiplas etapas)

Workflow: Actions > Agent — Propor melhoria editorial via IA > Run workflow.
Fica disponível no GitHub após este PR de infraestrutura ser integrado na main.

Entradas:
- kind: recipes ou techniques
- record_id: id existente em assets/data.js
- instruction: uma solicitação editorial objetiva, por exemplo "Tornar a explicação mais didática, preservando fatos".

Etapas: ler registro → validar contrato → IA reescreve somente campos textuais permitidos → valida novamente → rodar testes → criar branch → abrir PR draft → solicitar QA completo → esperar aprovação humana.

O agente de proposta NÃO altera IDs, ingredientes, quantidades, etapas de preparo, links, datas ou autoria. Sugestões da IA não comprovam fatos e devem ser revisadas.

Para funcionar:
- Configurar OPENAI_API_KEY em Settings > Secrets and variables > Actions.
- Configurar Settings > Actions > General > Workflow permissions para permitir que GitHub Actions crie PRs (dependendo das políticas do repositório).
- Nunca colocar a chave nos comandos ou no repositório.
- Se o GitHub bloquear criação de PRs pelo token automático, o workflow falhará de forma visível, sem integrar a alteração.

## Agent 3: Publicação segura (publisher-agent)

1. O responsável revisa diff, fontes, relatório de CI e possível auditoria IA.
2. O responsável integra o PR manualmente.
3. O workflow Publicar Dantas Cozinha, acionado por push na main, roda todo o harness e o navegador de teste.
4. Somente se tudo passar, a etapa dependente publica GitHub Pages.
5. Se falhar, a publicação NÃO é feita e o relatório release-quality-report estará disponível em Actions.

A automação antiga de republicação semanal sem alterações foi retirada do workflow de deploy; agora o deploy depende de alterações na main ou acionamento manual.

## Aprovação obrigatória: proteção de branch

O código impede auto-merge pelos agentes, mas **não impede que uma pessoa com acesso faça push direto à main**. Para tornar a aprovação obrigatória na infraestrutura do GitHub, configurar:

1. Repositório > Settings > Branches ou Rules > Rulesets > criar regra para main.
2. Require a pull request before merging (exigir PR).
3. Require status checks to pass (selecionar check validar, da workflow Validar curadoria e interface).
4. Bloquear bypass e pushes diretos conforme permissões disponíveis.
5. Opcional: exigir 1 aprovação de outro colaborador. O GitHub não permite que o autor do PR aprove a própria alteração, então isso exige um revisor distinto.

Para o projeto com apenas um mantenedor, a decisão manual de merge é o ponto de aceite, mas não equivale a revisão independente. O administrador deve decidir se exigirá segundo revisor.

## Diretrizes de conteúdo

Consultar .agents/skills/content-standards/SKILL.md. O validador também possui testes negativos para quantidade ausente, ID/título duplicado, aula incompleta, URL insegura e oficinas expiradas.

## App Store

A publicação iOS está **em pausa**. O PR anterior #3 é independente, não deve ser integrado por este trabalho.

## Limitações

- A IA de auditoria não pesquisa a web sozinha e não verifica veracidade de URLs.
- Sem OPENAI_API_KEY, o componente IA é pulado (claramente reportado).
- Testes automatizados não substituem revisão humana dos direitos de imagem, fonte e qualidade culinária.
- Proteção de branch exige configurar a regra no GitHub; não foi ativada automaticamente.
