from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    number = Column(String, unique=True)
    password = Column(String, nullable=False)

    pedidos = relationship("Order", back_populates="cliente")
