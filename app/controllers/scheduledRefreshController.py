# API Refresh Schedule
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-schedule

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

import requests
from datetime import datetime

import database.postgres.main as database
import Manage_Token.index as tkn
import app.models.scheduledRefreshModel as dataModel

# Recuperando informações do Banco
try:
    conn = database.PgConnect()

    # Definindo o cursor e fazendo consulta
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM datasets")
    db_return = cur.fetchall()

    # Enceranod conexão com o banco
    cur.close()
    conn.close()

    connected = True
except Exception as err:
    print(f"scheduleRefreshController :: Conexão/Leitura do banco de dados :: ERROR => {err}")
    connected = False


if connected == True:
    
    # Definindo parametros para fazer o requests na API
    access_list = tkn.Token_Manager()

    token_type = access_list["token_type"]
    token = access_list["access_token"]

    header = {
            "Authorization": f"{token_type} {token}"
            }
    
    # antes de iniciar apaga os dados da tabela
    try:
        conn = database.PgConnect()

        cur = conn.cursor()
        cur.execute('DELETE FROM scheduled_refresh')
        conn.commit()

        cur.close()
        conn.close()
    except Exception as err:
        print(f'scheduledRefreshController :: Delete from scheduled_refresh :: ERROR => {err}')

    for datasetId, name in db_return:

        url = f'https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/refreshSchedule'

        response = requests.request("GET", url, headers= header)

        if response.status_code == 200:
            res = response.json()
            refreshes_times = res["times"]
            is_active = res["enabled"]
            
            created_at = datetime.now()

            for refresh in refreshes_times:

                # mudando tipo de dado no item horario de atualização
                try:
                    insert = {
                            "dataset_name": f'{name}',
                            "dataset_id": f'{datasetId}',
                            "scheduled_refresh": refresh,
                            "is_active": f'{is_active}',
                            "created_at": f'{created_at}'
                            }
                    
                    print(f'{insert}\n')

                except Exception as err:
                    print(f"Something went wrong :: ERROR => {err}")

else:
    print("scheduleRefreshController :: Não foi possivel conectar ao banco")
