import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

load_dotenv()
# Acceder a las variables de entorno cargadas
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

meta = MetaData()

conn = engine.connect()