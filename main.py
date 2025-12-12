from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações JWT
SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Importando Models
from models.client import Client
from models.store import Store
from models.product import Product
from models.order import Order

# Importando Schemas
from schemas.client import ClientCreate, ClientResponse
from schemas.store import StoreCreate, StoreResponse
from schemas.product import ProductCreate, ProductResponse
from schemas.order import OrderCreate, OrderResponse

try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {str(e)}")


# Inicializando FastAPI
app = FastAPI(title="API Supermark")

# Dependência para usar sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções para login e hash
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# -----------------------
# ROTAS CLIENTE
# -----------------------
@app.post("/clientes/", response_model=ClientResponse)
def criar_cliente(cliente: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == cliente.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = hash_password(cliente.password)
    novo_cliente = Client(
        nome=cliente.nome,
        email=cliente.email,
        number=cliente.number,
        password=hashed_password
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

# -----------------------
# ROTAS LOJA
# -----------------------
@app.post("/lojas/", response_model=StoreResponse)
def criar_loja(loja: StoreCreate, db: Session = Depends(get_db)):
    existing_email = db.query(Store).filter(Store.email == loja.email).first()
    existing_cnpj = db.query(Store).filter(Store.cnpj == loja.cnpj).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if existing_cnpj:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    hashed_password = hash_password(loja.password)
    nova_loja = Store(
        nome=loja.nome,
        email=loja.email,
        endereco=loja.endereco,
        cnpj=loja.cnpj,
        password=hashed_password
    )
    db.add(nova_loja)
    db.commit()
    db.refresh(nova_loja)
    return nova_loja

# -----------------------
# ROTAS LOGIN
# -----------------------
@app.post("/login/cliente")
def login_cliente(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    cliente = db.query(Client).filter(Client.email == email).first()
    if not cliente or not verify_password(password, cliente.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    token = create_access_token({"sub": cliente.email, "tipo": "cliente"})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login/loja")
def login_loja(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    loja = db.query(Store).filter(Store.email == email).first()
    if not loja or not verify_password(password, loja.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    token = create_access_token({"sub": loja.email, "tipo": "loja"})
    return {"access_token": token, "token_type": "bearer"}

# -----------------------
# ROTAS PRODUTO
# -----------------------
@app.post("/produtos/", response_model=ProductResponse)
def criar_produto(produto: ProductCreate, db: Session = Depends(get_db)):
    loja = db.query(Store).filter(Store.id == produto.id_loja).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    novo_produto = Product(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        desconto=produto.desconto,
        id_loja=produto.id_loja
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# -----------------------
# ROTAS PEDIDO
# -----------------------
@app.post("/pedidos/", response_model=OrderResponse)
def criar_pedido(pedido: OrderCreate, db: Session = Depends(get_db)):
    cliente = db.query(Client).filter(Client.id == pedido.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    produto = db.query(Product).filter(Product.id == pedido.id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    novo_pedido = Order(
        id_cliente=pedido.id_cliente,
        id_produto=pedido.id_produto,
        quantidade=pedido.quantidade
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

# -----------------------
# ROTAS GET
# -----------------------
@app.get("/clientes/", response_model=list[ClientResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.get("/lojas/", response_model=list[StoreResponse])
def listar_lojas(db: Session = Depends(get_db)):
    return db.query(Store).all()

@app.get("/produtos/", response_model=list[ProductResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/pedidos/", response_model=list[OrderResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Order).all()
