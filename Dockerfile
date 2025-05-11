# Utilização da distribuição Debian Bookworm com o Python na versão 3.12 mais recente instalada
FROM python:3.12-bookworm

# Variável para o poetry não criar um virtual environment
#ENV POETRY_VIRTUALENVS_CREATE=false

# Definição do diretório app como raiz
WORKDIR /app
COPY . .

# Instalação do Google Chrome (última versão estável)
#RUN apt-get update && apt-get install -y wget unzip
#RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Download e descompatação do Google Chrome WebDriver compatível com a versão do Google Chrome instalada
#RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/$(google-chrome --version | awk '{print $3}')/linux64/chromedriver-linux64.zip" && unzip chromedriver-linux64.zip -d /usr/local/bin/ && rm chromedriver-linux64.zip

# Instalação do poetry
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && echo "$ENVIRONMENT"

# Instalação das dependências do projeto via poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Exposição da porta 8000 para a API
EXPOSE 8000

# Inicialização do fastapi
CMD ["poetry", "run", "fastapi", "run", "app/main.py"]
