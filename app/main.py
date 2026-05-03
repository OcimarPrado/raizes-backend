from fastapi import FastAPI
from app.api.routers import usuario_router, auth_router, produto_router

# Criação da aplicação principal. É aqui que o sistema ganha um nome e começa a existir.
app = FastAPI(title="Raízes do Nordeste API")

# --- REGISTRO DE ROTAS (Departamentos - Em vez de colocar 50 funções dentro de um arquivo só (o que seria uma bagunça),
# nós usamos os routers. Cada um cuida de um assunto: um para Usuários, um para Segurança (auth) e um para Produtos.) ---

# Se imaginarmos cada include_router como uma porta, teremos:

# Porta para cuidar de quem usa o sistema (Cadastro, Perfil)
app.include_router(usuario_router.router)

# Porta para a segurança: onde o usuário troca senha por um Token (A chave digital)
app.include_router(auth_router.router)

# Porta para o cardápio: onde gerenciamos os itens do Raízes do Nordeste
app.include_router(produto_router.router)


@app.get("/")
def read_root():
    """
    Esta é a rota de boas-vindas. 
    Se você acessar o endereço base da API, ela te responde que está viva e funcionando.
    """
    return {"message": "Bem-vindo à API Raízes do Nordeste!"}