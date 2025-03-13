from pydantic_settings import BaseSettings, SettingsConfigDict


#class Settings(BaseSettings):
#    # Especifica o arquivo contendo as informações necessárias para geração do token JWT (arquivo .env na raiz do projeto)
#    model_config = SettingsConfigDict(
#        env_file='.env', env_file_encoding='utf-8'
#    )
#
#    DATABASE_URL: str # Endereço para o Banco de Dados
#    SECRET_KEY: str #Secret Key
#    ALGORITHM: str #Algoritmo para assinatura do token JWT
#    ACCESS_TOKEN_EXPIRE_MINUTES: int #Tempo de expiração dos tokens JWT (em minutos)
#    DOWNLOAD_PATH: str  #Caminho para o diretório padrão de Downloads a ser utilizado pelo WebScrapper
#    NEW_NASDAQ_FILE: str  # Arquivo de relatório da Nasdaq
#    BASE_PATH: str # Caminho da raiz do projeto