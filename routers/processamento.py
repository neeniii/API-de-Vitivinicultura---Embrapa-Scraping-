from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
from scraper_direto.scraper import scraping


router= APIRouter( 
)

# Banco de dados de usuários em memória para autenticação
users = {
   "fiap": "fiap1",  # Usuário 1
}

security = HTTPBasic()


def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username in users and users[username] == password:
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Basic"},
    )




@router.get("/processamento",
            tags=["Processamento"],
    summary="Obter dados do processamento",
    description="Retorna os dados do processamento da vitivinicultura coletados do site da Embrapa. A consulta requer autenticação.")
def dados_processamento(username: str = Depends(verify_password)):
    
        return scraping("processamento")
        
def obter_dados(tipo: str):
    try:
        dados = scraping(tipo)
        return {"status": "sucesso", "dados": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))