from typing import Dict
from fastapi import FastAPI
from dotenv import load_dotenv
from app.auth.router import router as auth_router

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app: FastAPI = FastAPI(
    title="ERP Backend API",
    description="API REST para sistema ERP",
    version="1.0.0"
)

# Inclui rotas de autenticação
app.include_router(auth_router)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "ERP Backend API", "version": "1.0.0"}
