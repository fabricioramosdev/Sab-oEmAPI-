from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pandas as pd
import os

# Criação da aplicação FastAPI
app = FastAPI()

# Caminhos dos arquivos Parquet que simulam o banco de dados
MAQUINAS_PARQUET = "maquinas.parquet"
AGENDAMENTOS_PARQUET = "agendamentos.parquet"

# Modelo de dados para o agendamento
class AgendamentoInput(BaseModel):
    maquina_id: int              # ID da máquina a ser agendada
    horario: str                # Horário do agendamento (formato ISO 8601)
    cliente: str                # Nome do cliente

# Modelo de dados para adicionar nova máquina
class NovaMaquina(BaseModel):
    maquina_id: int              # ID único da máquina
    capacidade_kg: int           # Capacidade da máquina em quilos

# Endpoint para listar todas as máquinas
@app.get("/maquinas")
def listar_maquinas():
    df = pd.read_parquet(MAQUINAS_PARQUET)  # Lê o arquivo Parquet
    return df.to_dict(orient="records")    # Retorna lista de dicionários

# Endpoint para adicionar uma nova máquina de lavar
@app.post("/maquinas")
def adicionar_maquina(nova: NovaMaquina):
    df_maquinas = pd.read_parquet(MAQUINAS_PARQUET)  # Lê as máquinas existentes

    # Verifica se a máquina já existe
    if nova.maquina_id in df_maquinas["maquina_id"].values:
        raise HTTPException(status_code=400, detail="Máquina com esse ID já existe.")

    # Adiciona a nova máquina
    novo_df = pd.DataFrame([nova.dict()])
    df_maquinas = pd.concat([df_maquinas, novo_df], ignore_index=True)
    df_maquinas.to_parquet(MAQUINAS_PARQUET)  # Salva o novo estado

    return {"mensagem": "Máquina adicionada com sucesso."}

# Endpoint para agendar um horário em uma máquina
@app.post("/agendar")
def agendar_maquina(agendamento: AgendamentoInput):
    df_maquinas = pd.read_parquet(MAQUINAS_PARQUET)

    # Verifica se a máquina existe
    if agendamento.maquina_id not in df_maquinas["maquina_id"].values:
        raise HTTPException(status_code=404, detail="Máquina não encontrada.")

    try:
        data_hora_dt = datetime.fromisoformat(agendamento.data_hora)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data/hora inválido. Use ISO 8601.")

    df_agendamentos = pd.read_parquet(AGENDAMENTOS_PARQUET)

    # Verifica se já existe agendamento para essa máquina nesse horário
    conflitos = df_agendamentos[
        (df_agendamentos["maquina_id"] == agendamento.maquina_id) &
        (df_agendamentos["data_hora"] == agendamento.data_hora)
    ]

    if not conflitos.empty:
        raise HTTPException(status_code=409, detail="Horário já agendado para essa máquina.")

    # Adiciona o novo agendamento
    novo_agendamento = pd.DataFrame([{ 
        "maquina_id": agendamento.maquina_id, 
        "data_hora": agendamento.data_hora,
        "cliente": agendamento.cliente
    }])
    df_agendamentos = pd.concat([df_agendamentos, novo_agendamento], ignore_index=True)
    df_agendamentos.to_parquet(AGENDAMENTOS_PARQUET)

    return {"mensagem": "Agendamento realizado com sucesso."}



# Endpoint para consultar o status atual da máquina com base na hora atual
@app.get("/status/{maquina_id}")
def status_maquina(maquina_id: int):
    agora = datetime.now().replace(second=0, microsecond=0)

    df_agendamentos = pd.read_parquet(AGENDAMENTOS_PARQUET)
    df_maquina = df_agendamentos[df_agendamentos["maquina_id"] == maquina_id]

    # Se não há nenhum agendamento, está disponível
    if df_maquina.empty:
        return {"status": "disponivel"}

    df_maquina = df_maquina.copy()
    df_maquina["data_hora"] = pd.to_datetime(df_maquina["data_hora"])

    # Verifica se há agendamento para o horário exato atual
    ocupado = df_maquina[df_maquina["data_hora"] == agora]
    if not ocupado.empty:
        return {"status": "ocupado", "cliente": ocupado.iloc[0]["cliente"]}

    return {"status": "disponivel"}
