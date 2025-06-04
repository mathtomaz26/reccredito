from fastapi import FastAPI, Depends, Header, HTTPException
from pymongo import MongoClient
import os

# Inicializa o app
app = FastAPI()

# Lê variáveis do ambiente (definidas no EasyPanel)
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
API_KEY = os.getenv("API_KEY")

# Conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Middleware de autenticação
def verificar_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Token inválido")

# Rota 1
@app.get("/associados", dependencies=[Depends(verificar_token)])
def listar_associados():
    return list(db.todos_associados.find({}, {"_id": 0}))

# Rota 2
@app.get("/fichas-cobranca", dependencies=[Depends(verificar_token)])
def listar_fichas():
    return list(db.fichas_cobranca.find({}, {"_id": 0}))
