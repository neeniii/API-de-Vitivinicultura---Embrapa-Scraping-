import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# URLs das abas
URLS = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "importacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
    "exportacao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06",
}

# Caminho para os CSVs locais
CAMINHO_CSV = r"C:\Tech Challange\csv"

def scraping(tipo: str, ano_inicio=1970, ano_fim=2023):
    url_base = URLS.get(tipo.lower())
    if not url_base:
        raise ValueError(f"Aba inválida: {tipo}")

    dados = []

    try:
        for ano in range(ano_inicio, ano_fim + 1):
            print(f"Coletando dados do ano {ano}...")

            # Simula a requisição que o site faz ao selecionar um ano
            params = {'ano': ano, 'opcao': url_base.split('=')[-1]}
            response = requests.get("http://vitibrasil.cnpuv.embrapa.br/index.php", params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')

            if tables:
                # Converte a tabela HTML para DataFrame
                df = pd.read_html(str(tables[4]), flavor='bs4')[0]
                df["Ano"] = ano
                dados.append(df)

        if not dados:
            raise Exception("Nenhum dado coletado do site.")

        # Junta todos os dataframes e ordena por ano
        df_concat = pd.concat(dados, ignore_index=True)
        df_concat = df_concat.sort_values(by="Ano")
        df_concat.replace([np.inf, -np.inf], None, inplace=True)
        df_concat.fillna(0, inplace=True)

        return df_concat.to_dict(orient="records")

    except Exception as e:
        print(f"Erro no site: {e}")
        print(f"Carregando dados do CSV local da aba {tipo}...")

        caminho_arquivo = os.path.join(CAMINHO_CSV, f"{tipo.lower()}.csv")
        if os.path.exists(caminho_arquivo):
            try:
                df = pd.read_csv(caminho_arquivo, sep=";", encoding="utf-8-sig")
                df.replace([np.inf, -np.inf], None, inplace=True)
                df.fillna(0, inplace=True)
                print("Dados carregados do CSV local.")
                return df.to_dict(orient="records")
            except Exception as e_csv:
                raise Exception(f"Erro ao ler o CSV local: {e_csv}")
        else:
            raise Exception(f"O site está offline e o CSV local da aba {tipo} não foi encontrado.")