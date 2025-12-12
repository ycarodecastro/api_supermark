from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis de ambiente
USER = os.getenv("DB_USER")  # Usuário do banco de dados
PASSWORD = os.getenv("DB_PASSWORD")  # Senha do banco de dados
HOST = os.getenv("DB_HOST")  # Endereço do host do banco de dados
PORT = os.getenv("DB_PORT")  # Porta do banco de dados (geralmente 5432 para PostgreSQL)
DATABASE = os.getenv("DB_NAME")  # Nome do banco de dados

# Conexão PostgreSQL com SQLAlchemy
DATABASE_URL = "postgresql://supermarkdb_user:9hlMDiDyF5Vm8xbZ5RvMhdbrX65WBPek@dpg-d4tmmiemcj7s7382qs20-a.ohio-postgres.render.com/supermarkdb"

# Criando o engine de conexão com o banco
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para as classes do ORM
Base = declarative_base()

