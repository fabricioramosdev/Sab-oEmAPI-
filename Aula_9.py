from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Estrutura simples para armazenar as máquinas de lavar (em memória)
maquinas = {
    1: {"capacidade_kg": 10},
    2: {"capacidade_kg": 15},
    2: {"capacidade_kg": 18}
}

# Modelo para entrada de dados
class Maquina(BaseModel):
    capacidade_kg: int

# GET – Listar todas as máquinas
@app.get("/maquinas")
def listar_maquinas():
    return maquinas

# GET – Obter uma máquina específica
@app.get("/maquinas/{maquina_id}")
def obter_maquina(maquina_id: int):
    if maquina_id not in maquinas:
        raise HTTPException(status_code=404, detail="Máquina não encontrada.")
    return maquinas[maquina_id]

# POST – Adicionar nova máquina
@app.post("/maquinas")
def adicionar_maquina(maquina_id: int, maquina: Maquina):
    if maquina_id in maquinas:
        raise HTTPException(status_code=400, detail="Máquina já existe.")
    maquinas[maquina_id] = maquina.dict()
    return {"mensagem": "Máquina adicionada com sucesso."}

# PUT – Atualizar uma máquina existente
@app.put("/maquinas/{maquina_id}")
def atualizar_maquina(maquina_id: int, maquina: Maquina):
    if maquina_id not in maquinas:
        raise HTTPException(status_code=404, detail="Máquina não encontrada.")
    maquinas[maquina_id] = maquina.dict()
    return {"mensagem": "Máquina atualizada com sucesso."}

# DELETE – Remover uma máquina
@app.delete("/maquinas/{maquina_id}")
def deletar_maquina(maquina_id: int):
    if maquina_id not in maquinas:
        raise HTTPException(status_code=404, detail="Máquina não encontrada.")
    del maquinas[maquina_id]
    return {"mensagem": "Máquina removida com sucesso."}


# pip install fastapi uvicorn
# uvicorn Aula_9:app --reload
# http://localhost:8000/docs