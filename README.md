# XGBoost - Seleção Otimizada de Candidatos

O projeto foi pensado para otimizar o processo de seleção de candidatos de uma consultoria de RH, direcionando o melhor candidato para a vaga mais compatível, utilizando um modelo preditivo baseado no XGBoost.

Para isso, os dados foram recebidos em arquivos JSON, contendo informações estruturadas sobre candidatos e vagas. Durante a preparação dos dados, foi realizada a geração de embeddings no campo de descrição do currículo (cv_pt), transformando o texto em vetores numéricos que enriqueceram a base de dados.

Em seguida, foi realizada a limpeza dos dados, normalização, engenharia de atributos e a modelagem com o XGBoost, escolhido por sua alta performance, capacidade de lidar com dados heterogêneos e robustez contra overfitting. O modelo foi treinado para classificar candidatos conforme a sua compatibilidade com cada vaga.

Todo esse processo foi encapsulado em uma solução modular, permitindo fácil integração com APIs e automação do fluxo de seleção.

### Link Video:

- [Video Explicativo do Projeto]()

## Configurações de ambiente

### Pré-requisitos:

- [Python 3.11+](https://www.python.org)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Instalação do docker:

fazer o download e instalar o [Docker Desktop](https://www.docker.com/products/docker-desktop/) e no CMD executar comando abaixo:
(Comando que possibilita a execução de comandos linux mesmo em ambiente Windows)

```
wsl --install
```

#### Executar comandos na pasta raiz do projeto:

Utilizar os comandos abaixo para buildar o docker:

```
docker --debug build -t "fiap_datathon" .
```

Para rodar o docker executar comando abaixo:

```
docker run -p 8000:8000 --rm -it -e DATABASE_URL=sqlite:///database.db -e ACCESS_TOKEN_EXPIRE_MINUTES=30 -e SECRET_KEY=b71dc0943459ff1e7e668af25342877d641a76967061ba620fc2da7104aa1b37 -e ALGORITHM=HS256 -e DOWNLOAD_PATH=/app -e NEW_NASDAQ_FILE=HistoricalData_1731547025648.csv fiap_datathon
```

## Como usar os Endpoints na API:

1. Abrir link http://127.0.0.1:8000/docs
2. Criar usuário: Users > Try it out > Ajustar json com username / email /senha > Execute
3. Clicar em Authorize
4. Colocar email e senha

### 1º Endpoint: Autenticação /auth/token

- Autentica o usuário por meio de e-mail e senha

### 2º Endpoint: Users - Criar usuário

- Cria usuário para autenticação

### 3º Endpoint: Data-processing

- Executa funções de tratamentos de dados e prepara os Dataframes em uma pasta

### 4º Endpoint: Train - Treino

- Treina o modelo com o Dataframe fornecido

### 5º Endpoint: Previsão - Predict

- Realiza a previsão e mostra o resultado do modelo

## Funcionalidades Aplicadas

### Docker
Para garantir a portabilidade do ambiente de desenvolvimento e produção através de:
- Isolamento, containers contendo todas as dependências e configurações necessárias para o projeto, sem interferência por outros softwares;,
- Execução padronizada, da mesma forma em qualquer lugar (máquina local, servidor de desenvolvimento ou de produção, etc);,
- Gerenciamento de dependências, através do poetry para assegurar que as versões corretas das bibliotecas sejam instaladas.,
- Implantação consistente, pois a imagem docker já encapsula todo o ambiente.

### CI (Integração Contínua)
Para automatizar a integração de código, testes e validações, detectando erros rapidamente. Isso acelera o desenvolvimento, reduz riscos e garante a entrega de software mais estável e confiável.

### CD (Entrega Contínua)
Para automatizar a entrega de software para produção, após o CI. Isso garante implantações rápidas e seguras, tornando possível a disponibilização contínua da versão mais recente do software aos usuários.

### FastAPI

Para permite construir APIs web de alta performance de forma rápida e eficiente. Seus principais ganhos incluem velocidade de desenvolvimento, validação automática de dados (graças ao Pydantic) e documentação interativa (Swagger/OpenAPI) integrada.

## Contribuidores

- Anderson Pereira - RM 357310
- Gabriel Brites - RM 357307
- Lucas Soares - RM 356607
- Renan Serpa - RM 357478
- Ruan Costa - RM 357702

