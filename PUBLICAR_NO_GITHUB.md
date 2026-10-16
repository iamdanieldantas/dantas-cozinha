# Publicar Dantas Cozinha — conta @iamdanieldantas

> O projeto foi configurado, mas **não está online até que a implantação termine na sua conta GitHub**.

## Opção A — Terminal (Mac ou Linux, com GitHub CLI instalado)

1. Descompacte o ZIP. Abra o Terminal dentro da pasta `dantas-cozinha` (que contém `index.html`).
2. Execute:

```bash
gh auth login
git init -b main
git add .
git commit -m "feat: publicar Dantas Cozinha"
gh repo create iamdanieldantas/dantas-cozinha --public --source=. --remote=origin --push
```

Se o repositório `iamdanieldantas/dantas-cozinha` já existir, **não execute `gh repo create`**. Verifique primeiro o conteúdo existente e combine o novo projeto com cuidado.

3. Abra [Settings → Pages](https://github.com/iamdanieldantas/dantas-cozinha/settings/pages), em **Build and deployment → Source**, escolha **GitHub Actions**.
4. Abra [Actions](https://github.com/iamdanieldantas/dantas-cozinha/actions) e confira se **Publicar Dantas Cozinha** concluiu com sucesso. Se necessário, entre no workflow e clique em **Run workflow**.
5. Depois de publicado, visite: <https://iamdanieldantas.github.io/dantas-cozinha/>.

## Opção B — Usando o navegador (sem Terminal)

1. Crie o repositório público com o nome exato `dantas-cozinha`: <https://github.com/new>.
2. Descompacte o ZIP, abra o repositório e escolha **Add file → Upload files**. Envie as pastas e os arquivos da pasta `dantas-cozinha` para a raiz do repositório, preservando os caminhos.
3. **Importante:** a pasta `.github/workflows/site.yml` é oculta. No Finder do Mac, pressione **Command + Shift + .** para exibir itens ocultos e certifique-se de que `.github` também foi enviada, pois ela ativa a publicação e a rotina semanal.
4. Abra [Settings → Pages](https://github.com/iamdanieldantas/dantas-cozinha/settings/pages) e escolha **Source: GitHub Actions**.
5. Abra [Actions](https://github.com/iamdanieldantas/dantas-cozinha/actions), entre no workflow **Publicar Dantas Cozinha** e clique em **Run workflow** se for necessário. Aguarde a conclusão do deploy.
6. Acesse <https://iamdanieldantas.github.io/dantas-cozinha/>.

## Atualização semanal

- O GitHub Actions está preparado para rodar **segunda-feira, às 09h17 no horário de São Paulo**, sujeito a eventuais atrasos da plataforma.
- Sem chave, publica uma receita e uma técnica da fila editorial preparada, **enquanto houver itens disponíveis**.
- Para geração contínua por IA, configure o segredo **OPENAI_API_KEY** em [Settings → Secrets and variables → Actions](https://github.com/iamdanieldantas/dantas-cozinha/settings/secrets/actions). A API OpenAI tem cobrança própria. Não inclua a chave no código, em commits ou capturas de tela.
- O conteúdo de workshops/Instagram **não é atualizado automaticamente** nessa versão. Datas, preços e vagas devem ser conferidos nos canais das escolas.

## Privacidade

O portal será público. Favoritos, anotações pessoais e cardápio são armazenados no navegador de cada visitante (localStorage), sem conta ou sincronização entre aparelhos.

## Solução de problemas

- Página 404: verifique que Pages está em **GitHub Actions**, que o workflow concluiu, que a URL corresponde a `/dantas-cozinha/` e que o repositório está público.
- Workflow ausente: confira a pasta oculta `.github/workflows/site.yml` e que o branch principal se chama `main`.
- Falha ao gravar atualização: verifique permissões de **Actions** (`Read and write permissions`), proteção de branch e logs do workflow.
- API ausente: a geração contínua por IA não funciona sem configurar `OPENAI_API_KEY`; a fila editorial finita continua disponível.
