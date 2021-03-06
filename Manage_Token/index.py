import sys
sys.path.append('..')

import time

from database.firebase import main


# Gera novo token e salva no firebase
def postToken(db):
    # Faz a importação dentro da função para executar somente quando for chamado
    from Manage_Token import getToken
    
    # Recupera os dados para inserir no banco
    data = getToken.tokens

    # Insere os valores no banco
    db.collection('API').document('token').set(data)
    print('Manage_Tokens/index.py :: Dados novos inseridos no banco')


# Faz a consulta ao banco de dados e retorna 
def getToken(db):
    query = db.collection('API').document('token').get()
    query = query.to_dict()
    return query


# Gerencia se vai criar novo token ou usar existente
def Token_Manager():
    # Precisa receber o path do arquivo que chama a função até a pasta database
    # Criando conexão com o firestore
    db = main.DB_Conn()

    # Recuperar do banco hora que expira a chave
    db_query = getToken(db)
    expires_on = db_query["expires_on"]

    # Recupera a hora local para verificação, obs: para evitar possíveis erros atrasa em 5min o horario
    local_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time() - 300))

    # Verifica se o token está expirado
    if expires_on > local_time:
        return db_query
    else:
        postToken(db)
        query = getToken(db)
        return query

