from pydantic import BaseModel, EmailStr

class StoreBase(BaseModel):
    nome: str
    email: EmailStr
    endereco: str
    cnpj: str

class StoreCreate(StoreBase):
    password: str  # senha ao criar a loja

class StoreResponse(StoreBase):
    id: int

    class Config:
        orm_mode = True
