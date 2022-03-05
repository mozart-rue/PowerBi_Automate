# Import libraries
import os
from dotenv import load_dotenv
import requests

# Definindo credenciais para acesar a API 
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("KEYWORD")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
resource = "https://analysis.windows.net/powerbi/api"
grant_type = "password"
scope = "openid"

url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

body = {
'grant_type': f'{grant_type}',
'username': f'{username}',
'password': f'{password}',
'client_id': f'{client_id}',
'client_secret': f'{client_secret}',
'resource': f'{resource}',
'scope': f'{scope}'
}

headers = {
  'Cookie': 'fpc=AjmWF_rxL9ZGlDytx90M0WFiItQfAQAAAHzMtdkOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
}

# Fazendo a requisição POST na Azure para retornar token da API do power BI
response = requests.request(
    "POST",
    url=url,
    headers=headers,
    data=body
)

print(response.text)