---
name: portal-builder
description: Planejar, construir, testar, publicar e manter portais estáticos de conteúdo com GitHub Pages e atualizações editoriais verificáveis. Use quando for criar ou refinar outro portal a partir da arquitetura do Dantas Cozinha.
---

# Portal Builder — base reutilizável

## Objetivo
Construir portais de conteúdo com design responsivo, organização editorial, SEO básico, favoritos e personalização local opcionais, suíte de testes e CI/CD no GitHub Pages. Esta skill é independente do nicho: culinária, viagens, idiomas, estudos ou outros.

## Entradas obrigatórias
- `project_name`, `slug`, `github_owner`, `audience` (pessoal/público), `visual_theme`, `categories`.
- `content_sources`: autoridades editoriais e formas de verificar.
- `content_policy`: critérios de publicação, confiabilidade, origem e direitos de reprodução.
- `update_frequency`, `publication_mode` (revisão/automático) e `hosting`.

## Processo
1. **Descoberta**: perguntar objetivos, categorias, público, identidade visual, exemplos de referências e frequência de atualização.
2. **Schema de conteúdo**: definir IDs estáveis, categoria, título, descrição, autores, sourceName, sourceUrl, data de verificação e metadados particulares ao domínio.
3. **Curadoria**: consultar a fonte primária, abrir e verificar a URL, registrar autoria, ingredientes ou requisitos e não alegar aprovação/testes sem evidência. Conteúdo protegido deve ser referenciado, não copiado integralmente.
4. **Disponibilidade local**: considerar produtos/serviços disponíveis na localização de referência; itens raros apenas como opcionais e claramente sinalizados. Não confundir acessibilidade dos ingredientes com origem nacional do prato.
5. **Produto**: gerar cards, buscas, filtros, páginas detalhadas, links verificáveis, estados de erro, navegação móvel, acessibilidade e textos originais de interface.
6. **Personalização**: dados pessoais em localStorage apenas se houver aviso de que não sincronizam; criar backup/importação para não perder notas e favoritos.
7. **Qualidade**: testar schema, IDs exclusivos, URLs com protocolo HTTPS, categoria, sem campos enganosos; executar testes automatizados antes da publicação.
8. **Entrega**: criar branch, commits atômicos, pull request, revisar diff e somente então publicar na main pelo GitHub Actions.
9. **Automação**: agendar verificações semanais, evitar duplicação e nunca inventar fontes, eventos, preços, disponibilidade, avaliações ou alegações de teste. Sem dado válido, não publicar.
10. **Auditoria**: registrar data da atualização, fontes, itens publicados, exceções e status do workflow. Corrigir links indisponíveis.

## Convenções técnicas sugeridas
- Começar com HTML/CSS/JavaScript se o portal for estático, sem autenticação, com poucas seções.
- `index.html`, `assets/styles.css`, `assets/app.js`, `assets/data.js`, `tests/`, `.github/workflows/`.
- Migrar para framework/CMS/banco somente quando o requisito o justificar.
- GitHub Pages hospeda arquivos estáticos; APIs secretas devem ser chamadas via CI/backend, nunca a partir de código público no navegador.
- Usar `push main` para publicar, cron para revisão/atualização e `workflow_dispatch` para testes. Falha editorial não deve apagar conteúdo anterior.
- Não publicar dados pessoais ou segredos. Não automatizar scraping de redes sociais sem autorização e condições adequadas.

## Particularidades do exemplo Dantas Cozinha
- Receitas internacionais são bem-vindas; preferência por ingredientes normalmente vendidos em supermercados brasileiros.
- Receita publicada em fonte confiável **não** significa que foi testada pela equipe do portal.
- Fonte original e URL verificável obrigatórias; o preparo integral permanece na fonte, salvo autorização de reprodução.
- Categorias: entrada, principal, sobremesa; estudos, workshops, vídeos e planejamento complementares.
- Listas de compras só usam quantidades completas, verificadas e cadastradas; não estimar valores a partir de palavras-chave.

## Checklist de aceite
- [ ] Fontes verificadas e links clicáveis.
- [ ] Não há alegação injustificada de testes/aprovação.
- [ ] Categorias e navegação responsivas.
- [ ] Validação de dados e testes passando.
- [ ] Nenhum segredo no repositório.
- [ ] Branch/PR revisado, deploy concluído, URL testada.
- [ ] Atualização agendada e auditável.

## Prompt inicial para novo portal
"Use a skill portal-builder e o Dantas Cozinha como referência arquitetural, NÃO como dependência. Crie um portal chamado [NOME] sobre [ASSUNTO], para [PÚBLICO], com categorias [CATEGORIAS], tema [ESTILO], curadoria [FONTES], implantação em [OWNER/REPO] e frequência de atualização [CADÊNCIA]. Proponha schema, protótipo, testes, política editorial e pipeline antes de publicar."
