
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

def Insert_RefreshHistory(data): 

    dataset_name = data["dataset_name"]
    dataset_id = data["dataset_id"]
    status = data["status"]
    refresh_type = data["refresh_type"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    total_time = data["total_time"]
    request_id = data["request_id"]
    history_id = data["history_id"]
    inserted_at = data["inserted_at"]

    # Definindo query de inserção
    query = f"""INSERT INTO refresh_history (
                        dataset_name,
	                    dataset_id,
                        status,
                        refresh_type,
                        request_id,
	                    history_id,
                        started_at,
	                    ended_at,
                    	total_time,
	                    inserted_at
                        ) VALUES (
                        '{dataset_name}',
                        '{dataset_id}',
                        '{status}',
                        '{refresh_type}',
                        '{start_time}',
                        '{end_time}',
                        '{total_time}',
                        '{request_id}',
                        '{history_id}',
                        '{inserted_at}'
                        ); """

    # Criando conexão ao banco e aplicando a inserção
    try:
        conn = database.PgConnect()

        # Definindo cursor
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

        cur.close()
        conn.close()

        return True
    except Exception as err:
        print(f'refreshHistoryModel :: Inserindo dados no banco :: ERROR => {err}')
        return False

