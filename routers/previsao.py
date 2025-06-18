from fastapi import FastAPI
from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np


router= APIRouter( 
)

URLS_CSV = {
    "producao": "https://raw.githubusercontent.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-/main/csv/producao.csv",
    "processamento": "https://raw.githubusercontent.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-/main/csv/processamento.csv",
    "comercializacao": "https://raw.githubusercontent.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-/main/csv/comercializacao.csv",
    "importacao": "https://raw.githubusercontent.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-/main/csv/importacao.csv",
    "exportacao": "https://raw.githubusercontent.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-/main/csv/exportacao.csv",
}

def prever_para_tipo(url_csv):
    try:
        # Agora com separador ";" e encoding UTF-8
        df = pd.read_csv(url_csv, sep=";", encoding='utf-8')
        df.replace([np.inf, -np.inf], None, inplace=True)
        df.fillna(0, inplace=True)
        
        df.columns = [col.strip() for col in df.columns]
        df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce")
        df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
        df = df.dropna()

        if df.empty:
            return {"erro": "Dados insuficientes após limpeza."}

        X = df[["Ano"]]
        y = df["Quantidade"]

        X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelo = LinearRegression()
        modelo.fit(X_train, y_train)

        # Avalia o modelo com os dados de teste
        y_pred = modelo.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Erro médio quadrático: {mse:.2f}")

        anos_futuros = pd.DataFrame({"Ano": list(range(2024, 2029))})
        previsoes = modelo.predict(anos_futuros)

        return [{"ano": int(ano), "quantidade_prevista": float(q)} for ano, q in zip(anos_futuros["Ano"], previsoes)]

    except Exception as e:
        return {"erro": str(e)}
    
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

@router.get("/previsao")
def prever_todos():
    resultados = {}
    for tipo, url in URLS_CSV.items():
        resultados[tipo] = prever_para_tipo(url)
    return resultados