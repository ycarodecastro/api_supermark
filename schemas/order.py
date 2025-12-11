from pydantic import BaseModel

class OrderBase(BaseModel):
    id_cliente: int
    id_produto: int
    quantidade: int = 1

class OrderCreate(OrderBase):
    pass  # nada extra necessário ao criar

class OrderResponse(OrderBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode
