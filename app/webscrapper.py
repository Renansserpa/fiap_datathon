import os
import re
import time
from datetime import datetime

# from settings import Settings
from typing import Annotated

import dotenv
import pandas as pd
from fastapi import APIRouter, Depends
from selenium import webdriver
from selenium.webdriver.common.by import By

from .models import User
from .schemas import (
    NasdaqReportLine,
)
from .security import (
    get_current_user,
)

router = APIRouter(prefix='/webscrapper', tags=['webscrapper'])
CurrentUser = Annotated[User, Depends(get_current_user)]
# settings = Settings()
DOWNLOAD_PATH = os.environ['DOWNLOAD_PATH']
NEW_NASDAQ_FILE = os.environ['NEW_NASDAQ_FILE']


@router.post('/run/')
def webscrapper(
    current_user: CurrentUser,
    stock_alias: str = 'amzn',
):
    # Executa o script de webscrapper para a ação fornecida através do parâmetro stock_alias no website da Nasdaq.
    #   O histórico da ação disponibilizado através de Csv será obtido através de interação com o website via Selenium.
    #   Informações disponíveis no Csv da Nasdaq incluem Data, Fechamento, Volume, Abertura, Máxima e Mínima
    #
    # Argumentos:
    #   current_user: É um parâmetro contendo o usuário atual logado na API (se não estiver logado não será possível executar o script de webscrapper)
    #   stock_alias: É um parâmetro contendo o código da ação no website da Nasdaq, esta ação será o alvo do script de webscrapper
    #                   Por padrão, neste projeto foi utilizada a ação da Amazon (amzn)

    # Regex contendo padrão de nomenclatura igual a "HistoricalData_{timestamp}.csv" (sem aspas duplas)
    #   Onde {timestamp} representa o momento em que o arquivo foi gerado pelo sistema da Nasdaq (formato Unix Timestamp)
    #   Exemplo de nome de arquivo desejado: HistoricalData_1731329126102.csv
    _Pattern = re.compile(r'^HistoricalData_\d{13}\.csv$')

    # Enumerar arquivos da Nasdaq já existentes do diretório Downloads
    # O caminho para o diretório Downloads é especificado no arquivo de configuração do projeto (.env localizado na raiz do projeto)
    _NasdaqFiles = []
    with os.scandir(DOWNLOAD_PATH) as _DownloadsFiles:
        for _File in _DownloadsFiles:
            if _Pattern.match(_File.name):
                _NasdaqFiles.append(_File.name)

    # Criar webdriver (Chrome)
    # É necessário possuir o Google Chrome instalado, do contrário a execução do Script falhará
    _Driver = webdriver.Chrome()

    # Acessar URL da Nasdaq
    _Driver.get("https://www.nasdaq.com/market-activity/stocks/" + stock_alias + "/historical?page=1&rows_per_page=10&timeline=y10")

    # Aguardar 5 segundos para carregamento da página
    time.sleep(5)

    # Identificar botão para download de historico atraves do nome da classe
    _Button = _Driver.find_element(By.CLASS_NAME, 'historical-download')

    # Clicar no botão de download
    _Button.click()

    # Aguardar 5 segundos para concluir o download do relatório da Nasdaq
    time.sleep(5)

    # Encerrar webdriver
    _Driver.quit()

    # Identificar arquivo recém obtido da Nasdaq e armazenar seu nome de arquivo no sistema na variável NEW_NASDAQ_FILE do arquivo .env
    _NewNasdaqFile = ""
    with os.scandir(DOWNLOAD_PATH) as _DownloadsFiles:
        for _File in _DownloadsFiles:
            if _Pattern.match(_File.name) and _File.name not in _NasdaqFiles:
                dotenv_file = dotenv.find_dotenv()
                dotenv.load_dotenv(dotenv_file)
                os.environ["NEW_NASDAQ_FILE"] = _File.name
                dotenv.set_key(dotenv_file, "NEW_NASDAQ_FILE", os.environ["NEW_NASDAQ_FILE"])

    # Aguardar 15 segundos para concluir a atualização do arquivo .env em disco
    time.sleep(15)

    # Carregar o conteúdo do arquivo recém obtido da Nasdaq
    _NasdaqReportOnDisk = pd.read_csv(DOWNLOAD_PATH + '/' + NEW_NASDAQ_FILE, names=['Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low'])

    # Iniciar lista que conterá todas as linhas do arquivo recém obtido da Nasdaq
    _NasdaqReport = []

    # For para iterar através de cada uma das linhas do arquivo recém obtido da Nasdaq
    for i, row in _NasdaqReportOnDisk.iterrows():
        # Ignorar o cabeçalho de Csv
        if i != 0:
            _NasdaqReportLine = NasdaqReportLine(
                # Converter string para data
                date=datetime.strptime(row['Date'], '%m/%d/%Y'),
                # Remover o $ da célula, assim o conteúdo da célula será interpretado corretamente como float
                close=row['Close/Last'].replace('$', ''),
                # Remover o $ da célula, assim o conteúdo da célula será interpretado corretamente como int
                volume=row['Volume'].replace('$', ''),
                # Remover o $ da célula, assim o conteúdo da célula será interpretado corretamente como float
                open=row['Open'].replace('$', ''),
                # Remover o $ da célula, assim o conteúdo da célula será interpretado corretamente como float
                high=row['High'].replace('$', ''),
                # Remover o $ da célula, assim o conteúdo da célula será interpretado corretamente como float
                low=row['Low'].replace('$', ''),
            )
            # Adicionar o conteúdo da linha a lista
            _NasdaqReport.append(_NasdaqReportLine)
    # Retorna um JSON com todas as linhas do Csv
    return _NasdaqReport