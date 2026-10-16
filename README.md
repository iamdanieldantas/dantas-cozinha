# Dantas Cozinha 🍲

Portal pessoal de culinária, com visual acolhedor e **15 receitas iniciais completas**, técnicas, vídeos para inspiração, referências a escolas de gastronomia da Zona Sul de São Paulo, favoritos, notas e planejamento semanal com lista de compras.

## Testar agora

Abra `index.html` no navegador. Para publicar na conta `iamdanieldantas`, siga primeiro [PUBLICAR_NO_GITHUB.md](PUBLICAR_NO_GITHUB.md). A aplicação é um site estático sem instalação e sem servidor obrigatório, construído com HTML/CSS/JavaScript. Fotos ilustrativas exigem internet e têm fallback visual quando indisponíveis. Para servir em ambiente local:

```bash
python3 -m http.server 8080
# abrir http://localhost:8080
```

Os favoritos, as anotações, o cardápio e o checklist de compras ficam **somente no armazenamento deste navegador** (`localStorage`). É possível fazer backup/restaurar em **Meu cardápio → Exportar/Importar backup**. Eles NÃO sincronizam entre aparelhos. Não há login, conta de usuário nem banco de dados nesta versão.

## Publicar no GitHub Pages (passo a passo)

1. Na conta `iamdanieldantas`, crie um repositório **público** chamado `dantas-cozinha` e suba **todos os arquivos**, inclusive a pasta oculta `.github` (a branch padrão deve ser `main`).
2. Em **Settings → Pages → Build and deployment**, defina **Source: GitHub Actions**.
3. Em **Actions**, execute o workflow **Publicar Dantas Cozinha** caso o `push` inicial não tenha concluído a implantação.
4. Acesse a URL informada pelo GitHub Pages, normalmente `https://iamdanieldantas.github.io/dantas-cozinha/` (o endereço só existe após publicar).
5. **Atenção à privacidade:** o GitHub Pages não tem senha integrada neste pacote. O site e as receitas são publicamente acessíveis, embora os dados pessoais do navegador sejam locais. Se precisar de portal restrito, será necessário configurar autenticação/hospedagem apropriada (não basta ocultar a URL).

## Atualizações semanais — conteúdo e publicação

O arquivo `.github/workflows/site.yml` publica automaticamente às **09h17 de segunda-feira, horário de São Paulo**. O horário pode variar se a plataforma atrasar uma tarefa agendada. O fluxo:

1. Testa os dados existentes.
2. Executa `python scripts/weekly_update.py`.
3. Salva novos artigos/receitas no repositório quando houver mudanças.
4. Publica a versão resultante no GitHub Pages **no mesmo job**. Isso evita depender de um segundo workflow disparado pelo bot.

### Com geração nova por IA: atualização contínua (recomendado)

Configure um segredo chamado `OPENAI_API_KEY` em **Settings → Secrets and variables → Actions → New repository secret**. A chave **não** deve aparecer no código, em chats públicos ou em capturas de tela. A execução programada faz uma solicitação à API OpenAI (`gpt-4.1-mini` como padrão) para criar **uma receita e uma técnica culinária novas por semana**, submetidas a validações básicas antes de publicar. A API pode ter custo de uso, independente da assinatura do ChatGPT. É recomendado revisar periodicamente receitas geradas automaticamente por IA: a validação é de estrutura e plausibilidade básica, não é teste de cozinha nem checagem científica.

### Complemento de curadoria por ChatGPT

Além do GitHub Actions, há uma tarefa semanal do ChatGPT, configurada para as segundas-feiras à tarde (fuso de São Paulo). Ela confere se a publicação da semana ocorreu e tenta pesquisar e acrescentar conteúdos verificáveis de workshops, Instagram e vídeos, usando a integração GitHub quando disponível. Essa tarefa não é um processo executado no GitHub: sua execução e o acesso aos conectores dependem da disponibilidade da automação ChatGPT; se não conseguir publicar, deverá relatar o bloqueio. O workflow do GitHub Actions permanece como mecanismo principal e independente para publicação da receita e do estudo da semana.

### Sem chave de API: fila editorial finita

Sem `OPENAI_API_KEY`, a atualização semanal publica itens inéditos da fila `curatedQueue` em `assets/data.js`. **Essa fila se esgota**, então a publicação de novos conteúdos não é contínua: será necessário ampliá-la ou fornecer uma chave de API. O fluxo ainda pode republicar o site, mas não fingirá ter novas receitas.

### Rodar/testar a rotina manualmente

```bash
python3 -m unittest discover -s tests -v
python3 scripts/weekly_update.py --date 2026-10-19
```

**Cuidado:** o segundo comando modifica o conteúdo (não execute repetidamente em produção sem intenção). A rotina é idempotente para a mesma semana ISO.

## Conteúdo e fontes

Receitas e artigos iniciais são textos editoriais próprios, com imagens meramente ilustrativas carregadas do Unsplash. Endereços e escolas foram conferidos nas páginas oficiais em 15/10/2026:

- Accademia Gastronomica (Moema): https://www.agastronomica.com.br/ — https://www.instagram.com/agastronomica/
- IGA Vila Mariana: https://igavilamariana.com.br/
- Instituto Gourmet Santo Amaro: https://igsantoamarosp.com.br/

**Importante:** não são anúncios de cursos com vagas confirmadas. Datas, preços e vagas devem ser consultados diretamente nas escolas. A publicação automática nunca cria datas ou vagas de workshops, nem extrai posts do Instagram automaticamente. A seção Instagram oferece links externos de inspiração; incorporações automáticas de posts precisam de uma integração oficial e permissões da Meta.

## Estrutura

```text
index.html                  Página responsiva e abas
assets/styles.css           Visual acolhedor
assets/app.js               Favoritos, busca, notas, cardápio e lista
assets/data.js              Conteúdo publicado em JSON encapsulado em JS
scripts/weekly_update.py    Publicador e gerador de conteúdo
scripts/seed_content.py     Geração do conteúdo editorial inicial
.github/workflows/site.yml  CI, agenda semanal e deploy GitHub Pages
tests/                     Testes de conteúdo e atualização
```

Para modificar receitas manualmente, edite `assets/data.js` de modo que continue válido: `window.DANTAS_DATA = { ... };`. Evite rodar `scripts/seed_content.py` após começar a usar as atualizações semanais, pois ele reconstrói o conteúdo inicial.

## Limitações honestas

- O portal foi publicado no GitHub Pages em `https://iamdanieldantas.github.io/dantas-cozinha/`. Em caso de falha posterior, confira a aba Actions.
- A atualização via API depende da chave e do funcionamento do serviço. Se a API falhar, o sistema usa o conteúdo da fila editorial, caso ainda haja itens.
- Novos vídeos, eventos, vagas, posts do Instagram e informações de workshop **não são capturados automaticamente** nesta versão.
- A lista de compras soma unidades idênticas conforme o texto de cada ingrediente; itens parecidos descritos com palavras ou unidades diferentes aparecem separados. Refaça a conferência na prática.
