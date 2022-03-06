import sys
sys.path.append('..')

import time

from database.firebase import main

# Cria conexão com o firebase
db = main.db

# Gera novo token e salva no firebase
def postToken():
    # Faz a importação dentro da função para executar somente quando for chamado
    from Manage_Token import getToken
    
    # Recupera os dados para inserir no banco
    data = getToken.tokens

    # Insere os valores no banco
    db.collection('API').document('token').set(data)
    print('Manage_Tokens/index.py :: Dados novos inseridos no banco')


# Faz a consulta ao banco de dados e retorna 
def getToken():
    query = db.collection('API').document('token').get()
    query.to_dict()
    return query

