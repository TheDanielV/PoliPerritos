import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Cargar variables desde .env

DATABASE_URL = (
    f"mssql+pyodbc://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')},{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes&TrustServerCertificate=no"
    "&hostNameInCertificate=*.database.windows.net&loginTimeout=60"
)


# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase base para los modelos
Base = sqlalchemy.orm.declarative_base()

# Crear un sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
