from fastapi import FastAPI
from app.api.routers import usuario_router

app = FastAPI(title="Raízes do Nordeste API")

# Registrar rotas
app.include_router(usuario_router.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Raízes do Nordeste!"}