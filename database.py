from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ⚠️ Preencha com os dados do seu banco MySQL
USER = "root"
PASSWORD = "sua_senha"
HOST = "127.0.0.1"  # localhost ou IP remoto
PORT = "3306"  # porta padrão MySQL
DATABASE = "supermarkdb"

# Conexão MySQL com SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
