
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

# Criando funcao para inserir no banco
def Insert_Schedule(data):

    # recupera os dados
    dataset_name = data["dataset_name"]
    dataset_id = data["dataset_id"]
    is_active = data["is_active"]
    scheduled = data["scheduled_refresh"]
    inserted_at = data["created_at"]

    # define a query de inserção
    query = f"""INSERT INTO scheduled_refresh (
                    dataset_name,
                    dataset_id,
                    ativo,
                    atualizacao,
                    inserted_at
                    ) VALUES (
                    '{dataset_name}',
                    '{dataset_id}',
                    '{is_active}',
                    '{scheduled}',
                    '{inserted_at}'
                    );"""

    
