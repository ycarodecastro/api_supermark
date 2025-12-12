# Acessar a sessão do banco de dados
from database import SessionLocal
from main import criar_cliente


db = SessionLocal()

# Dados do novo usuário
nome = "João"
email = "joao@exemplo.com"
password = "senha123"  # Nunca use senhas simples assim em produção!
tipo = "cliente"

# Adicionar o usuário
novo_usuario = criar_cliente(nome, email, password, tipo, db)

# Exibir o usuário adicionado
print(f"Usuário {novo_usuario.nome} foi adicionado com sucesso!")
