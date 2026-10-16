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

## Política editorial vigente — receitas de fontes reconhecidas

A partir de 16/10/2026, as novas receitas do Dantas Cozinha serão selecionadas entre publicações de chefs, escolas de gastronomia e veículos culinários reconhecidos, com autoria e URL verificáveis, priorizando ingredientes brasileiros comuns ou regionais.

- **Nada de receitas inventadas por IA** ou alegações de teste sem confirmação da fonte. As 15 receitas iniciais permanecem como legado editorial **não testado/validado pela equipe** até eventual revisão.
- **Respeito à autoria:** resumir, dar crédito e apontar a fonte original; não reproduzir integralmente textos e imagens de terceiros sem autorização.
- A tarefa do ChatGPT faz curadoria **às segundas-feiras à tarde** e tenta atualizar o repositório quando encontra fontes confiáveis. A publicação de novos itens não é garantida se não houver material verificado ou a integração estiver indisponível.
- O workflow do GitHub Actions executa testes e publica o site quando houver commits, além de uma republicação agendada toda segunda de manhã. **Não executa mais o gerador anterior de receitas por IA/fila editorial.** O script `scripts/weekly_update.py` foi mantido apenas como legado.
- Para workshops e vídeos, usar links reais e não inventar datas, preços ou disponibilidade.

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
