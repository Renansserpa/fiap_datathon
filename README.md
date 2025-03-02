# Rede Neural (LSTM) - Amazon Stock

O projeto foi pensado para maximizar o ganho de uma ação em específico (No caso foi escolhida uma ação da Amazon) baseada em um modelo de rede neural preditivo do valor da ação em um período de 30 dias no futuro.

Para isso foi criada uma API para a coleta das informações da ação, após foi feita uma tratamento na base com relação a tipagem e limpeza de "Sujeiras", uma feature engineering com a geração de novos atributos que colaboraram para o treinamento do modelo e a utilização do modelo de rede neural LSTM (Long Short Term Memory) foi treinado o modelo de predição. Todo esse processo foi encapsulado em um container (docker).

### Link Video:

- [Video Explicativo do Projeto](https://youtu.be/f7wnxA9Gg5w)

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
poetry lock
docker --debug build -t "neural_net_amzn-docker" .
```

Para rodar o docker executar comando abaixo:

```
docker run -p 8000:8000 --rm -it neural_net_amzn-docker
```

## Como usar os Endpoints na API:

1. Abrir link http://127.0.0.1:8000/docs
2. Criar usuário: Users > Try it out > Ajustar json com username / email /senha > Execute
3. Clicar em Authorize
4. Colocar email e senha

### 1º Endpoint: Webscrapping

- Após a criação e autorização do usuário executar o edpoint.(Não é necessário parâmetros adicionais.)

### 2º Endpoint: Train_model

- Realizar o request com o envio de um Json contendo os hyper-parâmetros de pré-processamento e de modelo conforme no [schemas.py](neural_net_amzn-docker/schemas.py)

### 3º Endpoint: Predict_model

- Realizar o request com o envio de um Json-Dicionario representando o dataframe exportado pela nasdaq (Ação: amzn). Esses dados devem conter a data na qual se deseja receber a predição 30 dias no futuro e histórico até que o número de datas total seja igual ao comprimento de sequências que o modelo LSTM utiliza.

## Contribuidores

- Anderson Pereira - RM 357310
- Gabriel Brites - RM 357307
- Lucas Soares - RM 356607
- Renan Serpa - RM 357478
- Ruan Costa - RM 357702
