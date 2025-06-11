from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
from routers import producao, processamento, importacao, exportacao, comercializacao

app = FastAPI(title="API Produção Vitibrasil",
    description="API que faz scraping da embrapa",
    version="1.0.0")

app.include_router(producao.router)
app.include_router(processamento.router)
app.include_router(importacao.router)
app.include_router(exportacao.router)
app.include_router(comercializacao.router)


#Root - Verificar se está online
@app.get("/")
def root():
    return {"mensagem": "API embrapa"}
