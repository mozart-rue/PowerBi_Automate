# Importando Bibliotecas
import json
import time

# Importando arquivos
import main 

# Convertendo definitivamente o retorno da API em JSON
data = json.loads(main.response.text)

# Desconstruindo o retorno para uso das informações
api_token = data["access_token"]
token_type = data["token_type"]
refresh_token = data["refresh_token"]
token_id = data["id_token"]
expires_on = data["expires_on"]

# Formating fild expires_on to date and time
expires_on = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(expires_on)))

# Definindo dia e hora da criação do token
created_at = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())

# Criando objeto com as informações retornadas da API
tokens = {
        "access_token": f"{api_token}",
        "token_type": f"{token_type}",
        "refresh_token": f"{refresh_token}",
        "id_token": f"{token_id}",
        "created_at": f"{created_at}",
        "expires_on": f"{expires_on}"
        }

