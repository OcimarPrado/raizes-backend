from fastapi import FastAPI
from app.api.routers import usuario_router, auth_router

app = FastAPI(title="Raízes do Nordeste API")

# Registrar rotas
app.include_router(usuario_router.router)
app.include_router(auth_router.router)# Ativando o /auth/login

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Raízes do Nordeste!"}