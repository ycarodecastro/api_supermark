from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clients.id"), nullable=False)
    id_produto = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantidade = Column(Integer, default=1)
    data_compra = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Client", back_populates="pedidos")
    produto = relationship("Product", back_populates="pedidos")
