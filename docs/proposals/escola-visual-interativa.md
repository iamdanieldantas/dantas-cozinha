# Feature draft — Escola visual e interativa

Status: PROPOSTA / sem implementação. Data: 2026-11-10.

## Problema
As aulas atuais são longos blocos de texto, com poucos recursos para orientar leitura, comparação e entendimento de processos.

## Objetivo
Transformar a Escola em uma experiência didática visual e responsiva, preservando o conteúdo existente e a navegação atual.

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

## Plano de implementação (futuro PR separado)
1. Prototipar layout e componentes com dados do piloto.
2. Implementar renderizador e fallback legado.
3. Converter piloto para blocos tipados e revisar fontes/mídias.
4. Testar navegação, acessibilidade, desktop e mobile.
5. Executar `python -m harness.runner --mode review --browser`, registrar relatório e erros.
6. Abrir PR de implementação em rascunho; aprovação e merge exclusivamente humanos.

## Governança
Seguir AGENTS.md e as skills content-standards, quality-gates e release-approval. Nenhum commit na main, merge, deploy ou publicação automática. Este PR é apenas especificação; não altera o site.
