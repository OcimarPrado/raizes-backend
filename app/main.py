from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.api.routers import usuario_router, auth_router, produto_router, unidade_router, estoque_router, pedido_router
from app.api.routers.pagamento_router import router as pagamento_router
from app.api.routers.audit_log_router import router as audit_log_router
from app.api.exception_handlers import validation_exception_handler, integrity_error_handler, generic_exception_handler

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API de gerenciamento da rede de lanchonetes Raízes do Nordeste.",
    version="1.1.0"
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

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(produto_router.router)
app.include_router(unidade_router.router)
app.include_router(estoque_router.router)
app.include_router(pedido_router.router)
app.include_router(pagamento_router)
app.include_router(audit_log_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Raízes do Nordeste!", "docs": "/docs", "version": "1.1.0"}
