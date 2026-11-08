# Publicar o Dantas Cozinha na App Store sem possuir Mac

Objetivo confirmado: **iPhone**, **português (Brasil)**, **gratuito**, **conta individual (pessoa física)**. Repositório: iamdanieldantas/dantas-cozinha.

Esta preparação usa **Capacitor + Codemagic**. O GitHub Actions já validou a compilação **não assinada** para o simulador macOS. Isso NÃO é um arquivo IPA de distribuição, não dá acesso à conta Apple e não significa que o app foi publicado.

## 1. Inscrição Apple Developer Program (obrigatória)

Use a conta Apple com autenticação de dois fatores e seu nome civil correto. Em um iPhone compatível, instale o aplicativo Apple Developer, vá à aba Conta e escolha a opção para se inscrever. Se preferir, use https://developer.apple.com/programs/enroll/ . Escolha **Individual**, confirme os dados, faça verificação de identidade quando solicitada e pague a assinatura anual (US$ 99/ano, convertido/localizado onde disponível).

A Apple informa que, para conta Individual, o nome civil aparecerá como **vendedor** na App Store. "Dantas Cozinha" pode continuar como nome do aplicativo.

Não forneça senhas, códigos de verificação, chave .p8 ou certificados privados no ChatGPT ou no repositório.

## 2. Criar o app no App Store Connect

Depois que a inscrição estiver ativa e os contratos necessários forem aceitos:

1. Entre em https://appstoreconnect.apple.com/ .
2. Crie o identificador de aplicativo no Apple Developer, se ainda não existir: **com.iamdanieldantas.dantascozinha**. Se estiver indisponível, altere o identificador em capacitor.config.json **e** codemagic.yaml antes do primeiro build assinado.
3. Crie um novo aplicativo iOS no App Store Connect: nome **Dantas Cozinha**, idioma principal **Português (Brasil)**, Bundle ID selecionado e SKU único (ex.: dantas-cozinha-ios).
4. Configure como gratuito, categoria "Comida e bebida", dados de contato, país(es) de distribuição e classificação indicativa. Revise contratos exigidos.

Verifique disponibilidade do nome, categoria e Bundle ID na conta real; a existência não foi confirmada.

## 3. Conectar a conta Apple ao Codemagic — sem Mac

1. Entre em https://codemagic.io/ usando GitHub e autorize o acesso ao repositório dantas-cozinha.
2. Adicione o aplicativo ao Codemagic a partir do GitHub e selecione a branch com **codemagic.yaml**.
3. No App Store Connect, acesse Usuários e acesso > Integrações > API do App Store Connect. Gere uma chave dedicada, por exemplo "Dantas Codemagic", com permissão App Manager (ou a permissão exigida para seu fluxo). Guarde Key ID, Issuer ID e o arquivo .p8, que pode ser baixado apenas uma vez.
4. No Codemagic, conecte Developer Portal / App Store Connect usando essa chave, **exclusivamente nas telas seguras da plataforma**. Dê à integração o nome exato **dantas-app-store** porque é assim que o codemagic.yaml a referencia.
5. Em Code signing identities, configure um certificado **Apple Distribution** e um provisioning profile **App Store** correspondentes ao Bundle ID. O Codemagic pode auxiliar na geração/obtenção após a integração. Confirme que ambos aparecem cadastrados e vinculados ao Bundle ID.

**Não** adicione o arquivo .p8, certificados .p12 ou segredos ao Git, mensagens, issues ou prints.

Documentação oficial: https://docs.codemagic.io/yaml-quick-start/building-an-ionic-app/ e https://docs.codemagic.io/yaml-code-signing/signing-ios/ .

## 4. Executar build de distribuição e upload

A configuração está em **codemagic.yaml**, workflow **Dantas Cozinha — iOS para App Store Connect**.

- Executa npm install e os testes do pacote web.
- Gera o projeto iOS via Capacitor e cria ícones a partir do logo existente.
- Recupera a identidade de assinatura cadastrada no Codemagic.
- Compila o pacote .ipa de distribuição.
- Tenta enviar o build ao App Store Connect.

Por segurança, **submit_to_testflight: false** e **submit_to_app_store: false**. Isso evita acionar revisão ou publicação automaticamente. O arquivo .ipa, mesmo enviado, depende dos passos de cadastro/revisão no App Store Connect.

Se houver erro de signing, consulte os logs da execução para conferir App ID, certificado, profile e permissão do token, sem divulgar material secreto.

## 5. TestFlight e qualidade

No App Store Connect, depois que a Apple processar o build, adicione a versão no TestFlight e teste no iPhone real: abertura, navegação, compartilhamento, marcação de ingredientes, favoritos, notas, cardápio, backup e uso offline. Revise imagens e termos dos autores antes do envio público.

Uma aprovação técnica no CI **não substitui** testes no iPhone e não garante aprovação na Apple.

## 6. Materiais da App Store

Há rascunhos em **APP_STORE_METADATA_PT_BR.md** e **privacy.html**.

- O URL de privacidade será https://iamdanieldantas.github.io/dantas-cozinha/privacy.html **somente depois de incluir o arquivo na branch main e publicar o site**.
- Revise as declarações de privacidade do App Store Connect conforme as integrações reais; o armazenamento é local na versão inicial.
- Prepare capturas reais do aplicativo para os tamanhos de tela solicitados pela Apple.
- Confirme um canal de contato apropriado para suporte e política de privacidade; a URL de issues no GitHub é provisória.
- Confira classificação indicativa, direitos de uso de imagens e textos, disponibilidade por região e export compliance quando aplicável.
- O aplicativo poderá usar "Dantas Cozinha" como nome, mas o vendedor será o nome legal do titular da conta Individual.

## 7. Enviar para análise

Depois que todos os itens estiverem completos, selecione no App Store Connect o build processado, preencha os dados obrigatórios e envie para análise. A disponibilização na loja depende da aprovação da Apple; não há garantia de prazo ou aceite.

## O que precisamos do titular da conta

- Confirmar a inscrição Individual concluída e ativa.
- Conectar sua conta Apple ao Codemagic diretamente no serviço, sem divulgar segredos.
- Confirmar o nome legal exibido, o e-mail/canal de suporte e a ficha do aplicativo no App Store Connect.
- Revisar e aprovar materiais da loja e envio para análise.

**Status atual:** a base do projeto compila para simulador macOS no GitHub Actions; assinatura e envio à Apple não foram executados porque não há conta Developer conectada.
