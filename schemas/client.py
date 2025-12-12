from pydantic import BaseModel

class ClientBase(BaseModel):
    nome: str
    email: str

class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ClientCreate(BaseModel):
    nome: str
    email: str
    number: str
    password: str
