from pydantic import BaseModel

class StoreBase(BaseModel):
    nome: str
    email: str
    cnpj: str

class StoreResponse(StoreBase):
    id: int

    class Config:
        orm_mode = True


class StoreCreate(BaseModel):
    nome: str
    email: str
    endereco: str
    cnpj: str
    password: str
