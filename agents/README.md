# Agentes e harness do Dantas Cozinha

- editorial-reviewer: revisa conteúdo segundo a skill content-standards. IA opcional faz auditoria de registros existentes e produz um relatório com sugestões, nunca publica.
- qa-agent: usa a skill quality-gates, valida tipos, unitários, JavaScript e navegador; registra erros e bloqueia falhas.
- publisher-agent: usa release-approval, prepara PR com evidências e aguarda aprovação/merge humano. Depois do merge, GitHub Actions valida e publica.

Harness executável: harness/runner.py, com logs e relatório JSON.
Auditoria com IA: harness/ai_review.py; só executa modelo se OPENAI_API_KEY estiver configurada, sem alterar o catálogo.
Workflows: .github/workflows/agent-audit.yml e workflows de validação e publicação do site.

MCP é opcional: integração com o GitHub já é feita por workflows e APIs existentes; um servidor MCP pode ser acoplado depois.

Política: nenhum agente tem permissão para integrar alterações automaticamente.
