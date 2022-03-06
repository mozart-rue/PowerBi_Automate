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

created_at = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())

# Criando objeto com as informações retornadas da API
tokens = {
        "access_token": f"{api_token}",
        "token_type": f"{token_type}",
        "refresh_token": f"{refresh_token}",
        "id_token": f"{token_id}",
        "created_at": f"{created_at}"
        }

