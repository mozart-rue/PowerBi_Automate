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
    query = query.to_dict()
    return query


# Gerencia se vai criar novo token ou usar existente
def Token_Manager():
    # Recuperar do banco hora que expira a chave
    api_return = getToken()
    expires_on = api_return["expires_on"]

    # Recupera hora para verificação
    local_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())

    # Verifica se o token está expirado
    if expires_on > local_time:
        print('O Token está valido')
    else:
        print('Precisa gerar um novo token')

Token_Manager()
