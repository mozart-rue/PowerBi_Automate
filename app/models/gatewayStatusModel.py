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

import database.postgres.main as database

# Função que faz a inserção do dados 
def Insert_Gateways(data):
    
    # recuperando valores para inserir
    dataset_name = data["datasetName"]
    datasource_name = data["datasourceName"]
    datasource_id = data["datasourceId"]
    gateway_id = data["gatewayId"]
    gateway_name = data["gatewayName"]
    datasource_status = data["datasourceStatus"]
    inserted_at = data["insertedAt"]

    # Criando query de inserção dos dados
    query = f""" INSERT INTO gateways (
                        dataset_name,
	                    datasource_name,
	                    datasource_id,
	                    gateway_id,
                        gateway_name,
	                    datasource_status,
	                    inserted_at
                        ) VALUES (
                            '{dataset_name}',
                            '{datasource_name}',
                            '{datasource_id}',
                            '{gateway_id}',
                            '{gateway_name}',
                            '{datasource_status}',
                            '{inserted_at}'
                            );
                            """


