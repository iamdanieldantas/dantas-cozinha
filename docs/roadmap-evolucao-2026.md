# Plano de evolução — Dantas Cozinha

Status: execução por PRs incrementais, sujeitos a testes e aprovação explícita no chat para cada PR. Nenhuma aprovação genérica autoriza merges futuros.

## Princípios
- Preservar hospedagem estática até existir justificativa mensurável para backend ou framework.
- Respeitar fontes e direitos autorais; fichas de curadoria não se tornam receitas integrais sem licença.
- Componentes didáticos são opcionais, conforme a necessidade de cada aula.
- Cada mudança precisa de critérios de aceite, testes desktop/mobile, acessibilidade e rollback.
- A publicação só é considerada concluída após deploy e verificação da versão efetivamente servida.

## Fase 1 — Estabilidade e experiência básica (P0)
1. Pós-deploy: verificar HTML e hash dos três assets servidos pela URL pública, com retry e falha explícita; coberto por este PR.
2. Inventário de imagens e fontes: detectar links quebrados, registrar licença/crédito e exigir revisão visual humana de correspondência ao prato.
3. Navegação: verificar links diretos para receitas, retorno, estado do menu mobile, foco, contraste e teclado.
4. Qualidade: ampliar testes de navegador para componentes opcionais da Escola, estados vazios, responsividade e armazenamento local.
**Aceite:** CI e deploy verdes; nenhuma versão antiga de JS/CSS publicada; fluxos principais sem erro de console; nenhum recurso essencial depende de imagem externa.

## Fase 2 — Conteúdo e design (P1)
1. Escola: trilhas Fundamentos, Técnicas, Ciência e Prática; filtros e cards; aulas relacionadas.
2. Migrar editorialmente as 12 aulas existentes com recursos opcionais (imagens, tabelas, glossários, organogramas, passos, alertas) escolhidos por utilidade.
3. Receitas: revisão de quantidades, ingredientes, rendimento, preparo, fonte, foto e legenda; distinguir imagem ilustrativa.
4. Identidade: tokens, iconografia, hierarquia tipográfica, estados de interação e layout mobile.
5. Workshops e vídeos: separar escola permanente de evento com data, exibir data da última verificação; distinguir vídeo direto de busca.
**Aceite:** todas as aulas revisadas, sem placeholders vazios; fotos corretas ou explicitamente ilustrativas; direitos e fontes auditados; testes visuais desktop/mobile.

## Fase 3 — Arquitetura, performance e descoberta (P1/P2)
1. Extrair módulos JS por domínio, preservando compatibilidade do estado e backup.
2. Separar dados editoriais por domínio e validar com JSON Schema (ou equivalente) antes de compilar assets estáticos.
3. URLs compartilháveis por receita/aula, metadados por página, sitemap e dados estruturados quando comprovados.
4. Lazy loading de conteúdo e imagens, otimização de formatos, medição Lighthouse e budgets reais.
5. Busca unificada com navegação acessível, filtros e ranking básico.
**Aceite:** nenhuma perda de dados locais; deep links diretos funcionam; métricas de performance comparadas com baseline; QA passa.

## Fase 4 — Funcionalidades de aprendizado e cozinha (P2)
1. Modo estudo: progresso e conclusão por aula, persistência local e backup.
2. Modo cozinha: ingredientes marcáveis, etapas legíveis, timers e controle de tela.
3. PWA: manifest, ícones, cache offline limitado e estratégia de atualização segura.
4. Analytics com consentimento/privacidade e indicadores de utilidade, sem rastreamento invasivo.
**Aceite:** funcionamento mobile, acessibilidade, offline sem servir conteúdo obsoleto indefinidamente, dados exportáveis.

## Governança de PR
Cada PR descreve escopo, risco, dados afetados, evidência dos testes, impacto editorial, plano de rollback e screenshot quando visual. Branch de feature → harness → PR → aprovação específica no chat → merge permitido → publicação → smoke test. Não contornar proteções do GitHub.

## Indicadores
- Taxa de deploy bem-sucedido; divergências de asset após deploy; links/imagens quebrados.
- Cobertura de revisão editorial (aulas e receitas), fontes e créditos.
- Tempo de carregamento em celular, erros JS, problemas de acessibilidade.
- Uso do catálogo, Escola e planejamento, apenas se métricas forem adotadas com privacidade.
