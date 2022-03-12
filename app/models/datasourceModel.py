
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


# Função que faz a insercao dos dados na tabela

def Insert_Datasources(data):
    
    # Recuperando valores para inserir
    dataset_name = data["dataset_name"]
    dataset_id = data["dataset_is"]
    datasource_name = data["datasource_name"]
    conn_type = data["conn_type"]
    cred_type = data["cred_type"]
    gateway_id = data["gateway_id"]
    datasource_id = data["datasource_id"]
    inserted_at = data["inserted_at"]

    # Criando a query de inserção
    query = f""" INSERT INTO datasources (
                dataset_id,
	            dataset_nome,
	            datasource_nome,
        	    datasource_id,
	            gateway_id,
	            conection_type,
	            cred_type,
	            inserted_at
            ) VALUES (
                {dataset_id},
                {dataset_name},
                {datasource_name},
                {datasource_id},
                {gateway_id},
                {conn_type},
                {cred_type},
                {inserted_at}
            );
            """
           
    # Inserindo os dados no Banco
    try:
        # Cria conexão com o banco
        conn = database.PgConnect()

        # Define o cursor e executa a query
        cur = conn.cursor()
        cur.execute(query)
        cur.fetchall()

        # Encerra o cursor e a conexão
        cur.close()
        conn.close()

        # retorna concluido
        return True
    except Exception as err:
        print(f'Inserindo dados datasources: ERRO :: {err}')
        return False

