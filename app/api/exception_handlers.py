from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
'''
Verifica os erros e retorna ao usuário o codigo de erro e a mensagem de erro correspondente.
'''

def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"campo": " → ".join(str(loc) for loc in e["loc"]), "mensagem": e["msg"], "tipo": e["type"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"erro": "Dados inválidos na requisição.", "detalhes": errors})

def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={"erro": "Conflito de dados.", "detalhes": str(exc.orig)})

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"erro": "Erro interno no servidor."})
