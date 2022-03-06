# Importando Bibliotecas
import json
import pandas as pd
import time

# Importando arquivos
import main 

# Convertendo definitivamente o retorno da API em JSON
data = json.loads(main.response.text)

# Desconstruindo o retorno para uso das informações
api_token = data["access_token"]
token_type = data["token_type"]

# Recuperando o token
print(token_type)
print(api_token)

