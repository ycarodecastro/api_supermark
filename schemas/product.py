from pydantic import BaseModel

class ProductBase(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float
    desconto: float | None = 0.0  # desconto opcional
    id_loja: int  # relação com a loja

class ProductCreate(ProductBase):
    pass  # nada extra necessário ao criar

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode
