# API GET Refresh History
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-history


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
import Manage_Token.index as tkn

# Recuperando dados do banco para usar como parametro
try:
    conn = database.PgConnect()

    # Criando cursor
    cur = conn.cursor()

    # Executando query no banco
    cur.execute("SELECT id, name FROM datasets")
    db_return = cur.fetchall()

    # Encera a conexão com o banco de dados
    cur.close()
    conn.close()
    
    connected = True

except Exception as err:
    print(f'getRefreshHistoryController :: query select na base de dados :: ERRO => {err}')
    connected = False

if connected == True:
    print(db_return)

else:
    print('getRefreshHistoryController :: Erro => Não foi possivel executar a query no banco de dados')

