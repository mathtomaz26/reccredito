from fastapi import APIRouter, Depends, Header, HTTPException
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/fastapi-api/.env")  # <- aqui está o segredo

router = APIRouter()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
API_KEY = os.getenv("API_KEY")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def verificar_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Token inválido")

@router.get("/associados", dependencies=[Depends(verificar_token)])
def listar_associados():
    return list(db.todos_associados.find({}, {"_id": 0}))

@router.get("/fichas-cobranca", dependencies=[Depends(verificar_token)])
def listar_fichas():
    return list(db.fichas_cobranca.find({}, {"_id": 0}))

@router.get("/avisos-vencimento", dependencies=[Depends(verificar_token)])
def listar_avisos():
    return list(db.avisos_vencimento.find({}, {"_id": 0}))
