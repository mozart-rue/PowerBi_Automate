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

# Importando arquivo com função token
import Manage_Token.index as MT

# Recuperando dados de acesso
access_object = MT.Token_Manager()

# Definir parametros para consumir a API 
url = 'https://api.powerbi.com/v1.0/myorg/datasets'
token_type = access_object["token_type"]
token = access_object["access_token"]

header = {
        "Authorization": f"{token_type} {token}"
        }

response = requests.request("GET", url, headers=header )

print(response.text)

