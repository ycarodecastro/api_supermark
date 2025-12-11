from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    desconto = Column(Float, default=0.0)
    id_loja = Column(Integer, ForeignKey("stores.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    loja = relationship("Store", back_populates="produtos")
    pedidos = relationship("Order", back_populates="produto")
