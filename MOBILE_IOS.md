# Dantas Cozinha no iPhone — projeto inicial

Esta branch prepara o aplicativo iOS do Dantas Cozinha com Capacitor 8, sem mudar os arquivos do site em produção. A estrutura está pronta para gerar o projeto do Xcode; **ainda não houve compilação em Mac, instalação em iPhone nem publicação na App Store**.

## Recursos preparados

- Receitas, ingredientes, modos de preparo e aulas da Escola incluídos no aplicativo, com consulta dos textos mesmo sem conexão.
- Navegação inferior exclusiva do aplicativo: Início, Receitas, Escola, Oficinas e Cardápio.
- Compartilhamento de receitas e lista de compras com o plugin nativo Share da Apple (via Capacitor).
- Favoritos, notas, cardápio e checklist persistidos localmente no aplicativo.
- Aviso quando estiver offline. Fotos hospedadas fora do aplicativo, workshops e links externos precisam de internet.
- O projeto do site em GitHub Pages continua independente do aplicativo.

## Requisitos para gerar o aplicativo

- Mac com Node.js 22 ou superior.
- Xcode 26 ou superior e ferramentas de linha de comando (para Capacitor 8).
- Conta Apple para configurar assinatura e executar no iPhone; Apple Developer Program para distribuição na App Store.

## Primeira execução no Mac

Com o repositório clonado, selecione a branch feature/ios-capacitor-mvp-20261108 e execute no terminal:

    npm install
    npm run mobile:check
    npm run ios:add
    npm run ios:open

O comando ios:add cria o diretório nativo ios/; depois o Xcode abre o projeto.

No Xcode, selecione o target App, vá em Signing & Capabilities, configure seu Team Apple e um Bundle Identifier disponível. Escolha o simulador ou um iPhone conectado e clique em Run.

Para atualizar os arquivos do app depois de mexer no site ou nas receitas:

    npm run ios:sync
    npm run ios:open

Para executar no dispositivo/simulador a partir do terminal, após preparar o projeto nativo:

    npm run ios:run

O Bundle Identifier inicial sugerido em capacitor.config.json é com.iamdanieldantas.dantascozinha. Confirme a disponibilidade no seu Apple Developer Team antes de distribuir.

## Publicação na App Store — pendências

1. Compilar e testar a versão no simulador e num iPhone real.
2. Configurar ícone nativo, tela de abertura, aparência e assinatura digital.
3. Revisar os links externos, imagens, licenças das mídias e a experiência offline.
4. Preparar política de privacidade e declarações de coleta de dados compatíveis com o comportamento real da versão final.
5. Cadastrar o app no App Store Connect, testar pelo TestFlight e enviar para a análise da Apple.

A diretriz 4.2 da Apple exige valor além de apenas exibir um site. Esta base inclui navegação adaptada, conteúdo local e compartilhamento nativo, mas a aprovação não é garantida.

## Arquitetura e manutenção

- A origem do conteúdo continua em index.html e assets/ do projeto principal.
- scripts/build_mobile.mjs prepara a pasta www/, acrescenta estilos próprios do aplicativo e empacota o plugin Share via esbuild.
- npm run mobile:check valida os arquivos gerados e as aulas incluídas.
- A pasta www/ e as pastas geradas node_modules/ e ios/ não são versionadas nesta fase; o projeto iOS será criado localmente após instalação das dependências.
- Favoritos e anotações não sincronizam entre aparelhos. O backup local existente pode ter limitações na WebView e precisa ser testado em dispositivo.
- **Conteúdo atualizado no GitHub não chega sozinho ao app já instalado**: novas receitas exigem novo build por enquanto. Para atualizações silenciosas no futuro, será preciso implementar uma fonte remota de dados e cache offline adequados.

Documentação oficial: https://capacitorjs.com/docs , https://capacitorjs.com/docs/ios e https://developer.apple.com/app-store/review/guidelines/
