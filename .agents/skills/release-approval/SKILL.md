---
name: release-approval
description: Controlar publicação segura do Dantas Cozinha, exigindo revisão humana antes de integrar.
---

# Skill: guardião de publicação

Fluxo obrigatório: branch → validações → relatório → pull request → aprovação humana → merge manual → validação na main → GitHub Pages.

- O publisher-agent prepara PR e checklist; nunca executa merge ou push direto para main.
- Um erro interrompe o processo e mantém a versão anterior publicada.
- Exigir revisão de fonte, direitos de imagem e conteúdo antes da aprovação.
- O GitHub deve receber uma regra de proteção para main exigindo PR e checks; configurar no repositório por um administrador (este código sozinho não impede pushes manuais).
- Se houver apenas um mantenedor, o merge manual registra a decisão operacional; para aprovação formal de revisor distinto, habilitar regra e convidar colaborador.
- Não reabilitar a automação antiga de receitas por IA.
- Credenciais permanecem em GitHub Secrets; nunca expor em logs.
