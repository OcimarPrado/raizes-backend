from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import usuario_router, auth_router, produto_router, unidade_router, estoque_router, pedido_router

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API de gerenciamento da rede de lanchonetes Raízes do Nordeste.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(produto_router.router)
app.include_router(unidade_router.router)
app.include_router(estoque_router.router)
app.include_router(pedido_router.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Raízes do Nordeste!", "docs": "/docs"}
