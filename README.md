# API site embrapa - Dados da Vitivinicultura - produção, processamento, comerciaçização, exportação e importação
'''
API desenvolvida em FastAPI que realiza scraping dos dados do site da Embrapa das seguintes abas:

- Produção
- Processamento
- Comercialização
- Importação - Dados sobre (Vinhos de Mesa)
- Exportação - Dados sobre (Vinhos de mesa)
'''

## Funcionalidades
'''
- Raspagem direta via web scraping do site da Embrapa.
- Fallback para CSV local em caso de erro no scraping.
- Autenticação via HTTP Basic.
- Documentação automática via Swagger e ReDoc.
'''

## Documentação
'''
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
'''

## Autenticação
'''
A API utiliza autenticação HTTP Basic.

- Usuário: `fiap`
- Senha: `fiap1`
'''

## Endpoints (pontos de entrada ou endereços da API) Disponíveis
'''
| Método | Endpoint              | Descrição                          | Autenticado |
|--------|------------------------|-------------------------------------|--------------|
| GET    | `/`                    | Verifica se a API está online      | ❌           |
| GET    | `/producao`            | Dados de produção                  | ✔️           |
| GET    | `/processamento`       | Dados de processamento             | ✔️           |
| GET    | `/comercializacao`     | Dados de comercialização           | ✔️           |
| GET    | `/importacao`          | Dados de importação                | ✔️           |
| GET    | `/exportacao`          | Dados de exportação                | ✔️           |
'''
## Instalação e Execução

### Pré-requisitos
'''
- Python 3.9+
'''
### Instalação

1. Clone o repositório:

```bash
git (https://github.com/neeniii/API-de-Vitivinicultura---Embrapa-Scraping-)
cd API-de-Vitivinicultura---Embrapa-Scraping-

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   

4. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```



'''
## Estrutura do Projeto
'''
.
├── main.py                   # Arquivo principal da aplicação
├── scraper.py                # Lógica de scraping + fallback CSV
├── producao.py               # Endpoint: /producao
├── processamento.py          # Endpoint: /processamento
├── comercializacao.py        # Endpoint: /comercializacao
├── importacao.py             # Endpoint: /importacao
├── exportacao.py             # Endpoint: /exportacao
├── /csv                      # (Opcional) CSVs locais para fallback
└── README.md
'''

## Tecnologias Utilizadas
'''
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pandas](https://pandas.pydata.org/)
- [lxml](https://lxml.de/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [NumPy](https://numpy.org/)
- [Requests](https://docs.python-requests.org/)
- Autenticação via HTTP Basic
'''

## Observações
'''
- O scraping depende da estrutura atual do site da Embrapa.
- Caso o scraping falhe, os dados são carregados de arquivos CSV locais no caminho:

  C:\Tech Challange\csv\[aba].csv
  
'''

## Melhorias Futuras
'''
- Migração da autenticação para JWT.
- Cache em memória para anos já consultados.
- Pegar informações dos outros filtros que tem na aba importação e exportação, nessas abas, estou trazendo as informações do filtro Vinhos de mesa.

---

## 👨‍💻 Autor

Gabriel Pereira Ferreira
