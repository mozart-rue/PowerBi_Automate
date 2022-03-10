# API: GET DATASETS
# Doc: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasets#code-try-0


# ----------------------- ADD RAIZ DO PROJETO AO ARQUIVO  ----------------------- #
# Adicionando o path para a Raiz do projeto dinamicamente para fazer a importação de arquivos.py
import sys
import os

def Resolve_Path():
    # Recupera o diretorio atual e separa o ultimo iten
    current_path = os.getcwd() # --> retorna diretorio atual: ex: (main/path/to/folder)
    split_path = os.path.split(current_path) # --> retorna: (main/path/to, folder)
    head, tail = split_path # --> recupera os dois itens um para cada variavel (em ordem)

    # Encontra o path até a raiz do projeto (raiz = InfoCargas)
    while not head.endswith('InfoCargas'):
        split_path = os.path.split(head)
        head, tail = split_path

    return head

path = Resolve_Path()
sys.path.append(os.path.abspath(f"{path}"))
# ---------------------------------------------------------------------------------- #

# Importando bibliotecas python
import requests
import pandas as pd

# Importando arquivos
import Manage_Token.index as MT
import database.postgres.main as db_engine

# Recuperando dados de acesso
access_object = MT.Token_Manager()

# Definindo parametros para consumir a API 
url = 'https://api.powerbi.com/v1.0/myorg/datasets'
token_type = access_object["token_type"]
token = access_object["access_token"]

header = {
        "Authorization": f"{token_type} {token}"
        }


# Função que faz o Request a API de DATASETS e faz o tratamento da resposta
def GET_Datasets():
    # Fazendo o Request na API
    response = requests.request("GET", url, headers=header )

    # Quebrando o JSON de retorno
    json_data = response.json()
    data = json_data["value"]

    # Definindo o dataframe
    response_df = pd.DataFrame()

    # Inserindo os dados da API no Dataframe
    res_itens = pd.DataFrame.from_records(data)
    response_df = response_df.append(res_itens, ignore_index=True)

    # Filtrando os dados do Dataframe
    response_df = response_df[["id", "name", "webUrl", "isRefreshable", "isOnPremGatewayRequired"]]

    # Criar conexão com banco
    engine = db_engine.PgEngineConn()

    # Inserindo o dataframe no banco de dados
    try:
        response_df.to_sql('datasets', engine, if_exists='replace', index= False)
    except Exception as err:
        print(f'Inserindo dataframe no banco :: error: {err}')

GET_Datasets()
