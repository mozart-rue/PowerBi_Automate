# Criando Conector ao Banco de Dados Postgre
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Definindo as credenciais para acessar o banco
load_dotenv()
pg_host = os.getenv("PGHOST")
pg_user = os.getenv("PGUSER")
pg_key = os.getenv("PGKEY")
pg_db = os.getenv("PGDB")

# Criando Funções para conexão

# - Conexão por engine para usar com o pandas
def PgEngineConn():
    # definindo string de conexão ao Postgre
    pg_credentials = f'postgresql://{pg_user}:{pg_key}@{pg_host}/{pg_db}'

    # Criando a engine de conexão ao postgre
    pgConn = create_engine(pg_credentials)

    return pgConn

