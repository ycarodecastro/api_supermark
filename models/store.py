from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    produtos = relationship("Product", back_populates="loja")
