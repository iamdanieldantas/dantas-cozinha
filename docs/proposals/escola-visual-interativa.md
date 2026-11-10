# Feature draft — Escola visual e interativa

Status: PROPOSTA / sem implementação. Data: 2026-11-10.

## Problema
As aulas atuais são longos blocos de texto, com poucos recursos para orientar leitura, comparação e entendimento de processos.

## Objetivo
Transformar a Escola em uma experiência didática visual e responsiva, preservando o conteúdo existente e a navegação atual.

## Abrangência obrigatória: TODOS os artigos da Escola
Os recursos são **opcionais e combináveis por artigo**. Nenhuma aula é obrigada a conter imagens, bullets, workflows, organogramas ou exercícios. A infraestrutura deve oferecer esses tipos de bloco e o editor escolhe apenas os adequados ao tema. A entrega não é considerada concluída com apenas um piloto. O novo design system e renderizador devem servir a **100% dos artigos atuais** da coleção `window.DANTAS_DATA.techniques` e a qualquer artigo novo. O piloto é só a primeira etapa de validação; o rollout integral e a auditoria artigo por artigo fazem parte do mesmo objetivo da feature.

### Inventário atual (gerado a partir do catálogo)
- `escola-brigada-pracas-funcionamento` — Por dentro da cozinha profissional: cargos, praças e serviço
- `tec-1` — Mise en place: cozinhar sem correria
- `tec-2` — Maillard: o segredo do dourado
- `tec-3` — Emulsão: molhos mais cremosos
- `tec-4` — Como ajustar o sal sem errar
- `tec-5` — Fermento químico x bicarbonato
- `tec-6` — Manteiga noisette em casa
- `tec-7` — Segurança com frango
- `tec-8` — Três maneiras de engrossar molhos
- `tec-servico-refeicao` — Antipasto, entrada, couvert e aperitivo
- `tec-contaminacao-direta` — Contaminação direta dos alimentos
- `tec-contaminacao-cruzada` — Contaminação cruzada: direta e indireta

### Matriz de enriquecimento por artigo
- Para **cada artigo**, avaliar a pertinência de imagem, bullets, ícones, workflow, diagrama, comparativo, glossário e exercício; não forçar diagramas ou fotos quando não agregam clareza.
- Cada artigo deve manter uma estrutura editorial legível e flexível (título, resumo e seções; objetivos, prática e conclusão quando pertinentes). **Não exigir nenhum bloco visual específico**, nem quantidade mínima de imagens, listas, ícones ou diagramas.
- Criar inventário de migração com `id`, blocos planejados, fonte/crédito de mídia, status e resultado de QA por artigo.
- Exigir cobertura automatizada que derive a lista de IDs do catálogo e sinalize artigo não migrado; não fixar a quantidade de aulas no teste.
- Preservar significado e conteúdo técnico, revisar acessibilidade e licenciamento de cada mídia.

## Escopo do MVP
1. Página de aula com título, resumo, objetivos de aprendizagem, índice navegável e seções em blocos.
2. Renderizador de blocos tipados: paragraph, bulletList, numberedList, image, callout, iconFact, flowchart, orgChart, comparison, glossary, exercise.
3. Diagramas e fluxos em HTML/CSS/SVG acessível (com alternativa textual), responsivos no celular; sem depender de imagens geradas para explicar relações.
4. Imagens pertinentes com texto alternativo, legenda, créditos, licença e origem verificável; fallback quando indisponíveis; nunca usar imagem aleatória como evidência.
5. Ícones consistentes para funções, segurança, etapas, exemplos e dicas; ícones sempre acompanhados de texto.
6. Expansão/colapso de seções, progresso visual local não persistente, âncoras e navegação por teclado.
7. Preservar `window.DANTAS_DATA.techniques` e campos existentes; introduzir `contentBlocks` opcional com migração progressiva, sem quebrar aulas antigas.

## Piloto: Por dentro da cozinha profissional
- Organograma da brigada: chef executivo (quando existir) → chef de cuisine → sous-chef → chef de partie → commis/auxiliares; legenda de variações entre restaurantes.
- Mapa ilustrativo de praças: quente, fria, confeitaria, passe; responsabilidades, exemplos e equipamento.
- Workflow da comanda: salão → passe → praças → conferência → salão, com ramificações de entrada/principal/sobremesa.
- Cartões com termos franceses, exemplos práticos, erros comuns e mini exercício de associação.
- Diferenciar praça (estação) de cargo (função) e brigada clássica de operações modernas.

## Exemplo de estrutura de bloco (proposta, não contrato vigente)
```json
{"type":"flowchart","id":"fluxo-comanda","title":"Da comanda à mesa","steps":[{"id":"salon","label":"Salão registra pedido"},{"id":"passe","label":"Passe coordena"},{"id":"pracas","label":"Praças preparam"},{"id":"confere","label":"Passe confere"},{"id":"entrega","label":"Salão entrega"}],"accessibleDescription":"Pedido registrado no salão, coordenado pelo passe, preparado pelas praças, conferido e entregue."}
```

## Critérios de aceite
- Todos os artigos existentes continuam acessíveis, sem perda de conteúdo.
- Piloto tem ao menos um organograma, um fluxo e blocos com listas, ícones e imagens apenas quando direitos e pertinência forem verificados.
- Desktop e mobile sem rolagem horizontal; leitura e controles acessíveis por teclado, foco visível e descrições textuais dos diagramas.
- URLs e licenças de mídia auditáveis; imagens não verificadas não são incluídas.
- Sem links quebrados, exceções JS, regressão em hash navigation ou seções expansíveis.
- Dados e testes derivados do catálogo, sem quantidades fixas; sem afrouxar critérios para obter CI verde.

## Contrato de composição flexível
- `contentBlocks` é uma lista opcional de blocos heterogêneos; cada artigo pode ter zero ou mais instâncias de cada tipo permitido.
- O renderizador deve preservar a ordem dos blocos, permitir texto simples e renderizar aulas legadas sem `contentBlocks`.
- Campos opcionais ausentes não podem criar espaços vazios, placeholders ou erros.
- O catálogo pode conter aulas inteiramente textuais, aulas com uma imagem ou aulas com vários fluxogramas, conforme necessidade didática.
- Validar apenas a estrutura dos blocos **presentes** e os requisitos comuns; não impor um checklist de mídia por aula.

## Critério de conclusão global
**100% das aulas existentes compatíveis e verificadas** com o novo renderizador e padrão editorial, sem obrigatoriedade de adicionar todos os recursos a todas as aulas, além de template para futuras aulas. O piloto isolado não satisfaz o aceite. Validar a página de cada artigo em desktop e mobile e revisar mídia, diagramas e estrutura didática. Quando o conteúdo não pedir um fluxo, usar outra representação pertinente.

## Plano de implementação (futuro PR separado)
1. Prototipar layout e componentes com dados do piloto.
2. Implementar renderizador e fallback legado.
3. Converter piloto para blocos tipados e revisar fontes/mídias.
3a. Garantir compatibilidade de todas as demais aulas com o renderizador, migrando/enriquecendo somente onde fizer sentido editorial e revisando cada uma.
4. Testar navegação, acessibilidade, desktop e mobile.
5. Executar `python -m harness.runner --mode review --browser`, registrar relatório e erros, incluindo cobertura integral das aulas.
6. Abrir PR de implementação em rascunho; aprovação e merge exclusivamente humanos.

## Governança
Seguir AGENTS.md e as skills content-standards, quality-gates e release-approval. Nenhum commit na main, merge, deploy ou publicação automática. Este PR é apenas especificação; não altera o site.
