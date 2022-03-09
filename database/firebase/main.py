import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Função que retorna o path para o arquivo 'json' de autenticação do firebase
def Path_To_Json():
    # Recupera o diretorio atual e separa o ultimo iten
    current_path = os.getcwd() # --> retorna diretorio atual: ex: (main/path/to/folder)
    split_path = os.path.split(current_path) # --> retorna: (main/path/to, folder) 
    head, tail = split_path # --> recupera os dois itens um para cada variavel (em ordem)
    
    # Encontra o path até a raiz do projeto (raiz = InfoCargas)
    while not head.endswith('InfoCargas'):
        split_path = os.path.split(head)
        head, tail = split_path

    path_to_json = f'{head}/database/firebase/config/serviceAccountKey.json'

    return path_to_json
    

# Função que retorna a conexão com o firestore
def DB_Conn():
    # Recupera o path do arquivo JSON
    path = Path_To_Json()
    # Cria conexão com o firebase, recebe como parametro o arquivo JSON com a autenticação
    cred = credentials.Certificate(f'{path}')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    
    return db
