---
name: quality-gates
description: Criar e executar testes resistentes a mudanças do catálogo e impedir deploy com erros.
---

# Skill: validação e testes

1. Validar conteúdo via python -m harness.validate_content: schema, campos, datas, quantidade positiva, IDs únicos, HTTPS e autoria.
2. Rodar testes via python -m unittest discover -s tests -p 'test_*.py' -v.
3. Validar JavaScript via node --check assets/app.js e node --check assets/data.js.
4. Validar interface real em desktop e mobile via python tests/browser_smoke.py.

## Regras

- Nunca fixar quantidade de receitas, oficinas, vídeos ou aulas; derivar de window.DANTAS_DATA.
- Workshop expirado é dado histórico válido. O teste deve comparar com a filtragem efetiva pela data.
- Testes de fluxo devem confirmar receitas completas, navegação por hash, favoritos, aulas expansíveis e ausência de exceções JS.
- Falha bloqueia deploy. Não usar continue-on-error para ignorar testes.
- Registrar duração, saída, erro, exit code, branch, SHA e horário no relatório JSON do harness.
- Enviar relatório como artefato mesmo quando o job falhar; jamais expor secrets.
- PR precisa de CI verde e aprovação humana. O CI não faz merge.
