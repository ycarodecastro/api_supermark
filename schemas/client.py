from pydantic import BaseModel, EmailStr

class ClientBase(BaseModel):
    nome: str
    email: EmailStr
    number: str | None = None  # telefone opcional

class ClientCreate(ClientBase):
    password: str  # senha ao criar o cliente

class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True
