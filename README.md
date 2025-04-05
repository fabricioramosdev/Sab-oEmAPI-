# 📘 API de Lavanderia – Documentação Técnica

Bem-vindo à API de Lavanderia. Ela foi feita com FastAPI e salva os dados em arquivos Parquet porque, sei lá, banco de dados seria *muito mainstream*. Essa API permite listar máquinas, agendar horários e consultar status.

## https://sabaoemapi.onrender.com/docs

## 📦 Endpoints Disponíveis

### 1. **GET /maquinas**
Retorna todas as máquinas de lavar disponíveis, junto com sua capacidade em kg.

#### 📥 Requisição:
Sem parâmetros.

#### 📤 Resposta:
```json
[
  {
    "maquina_id": 1,
    "capacidade_kg": 10
  },
  {
    "maquina_id": 2,
    "capacidade_kg": 15
  }
]
```

---

### 2. **POST /agendar**
Agenda uma máquina de lavar para um horário específico. Evite conflitos, por favor.

#### 📥 Requisição:
```json
{
  "maquina_id": 2,
  "horario": "2025-04-04T14:00:00",
  "cliente": "Maria do Sabão"
}
```

- `maquina_id`: ID da máquina que deseja agendar.
- `horario`: Horário em formato ISO 8601.
- `cliente`: Nome do cliente (ou nome de guerra, tanto faz).

#### 📤 Resposta:
```json
{
  "mensagem": "Agendamento realizado com sucesso."
}
```

#### ⚠️ Possíveis Erros:
- `404`: Máquina não encontrada.
- `409`: Horário já agendado para essa máquina.

---

### 3. **GET /status/{maquina_id}**
Consulta o status atual da máquina (baseado na hora atual).

#### 📥 Parâmetro de caminho:
- `maquina_id`: ID da máquina que deseja consultar.

#### 📤 Resposta:
```json
{
  "status": "disponivel"
}
```

ou

```json
{
  "status": "ocupado",
  "cliente": "Maria do Sabão"
}
```

---

## 🧪 Testar a API
Você pode brincar com ela via Swagger em:
```
http://localhost:8000/docs
```

Ou, se você se acha melhor que isso:
```
http://localhost:8000/redoc
```

---

## 📝 Notas Finais
- Dados são armazenados em arquivos Parquet (`maquinas.parquet`, `agendamentos.parquet`).
- Agendamentos são registrados por hora cheia (sem intervalo de tempo, sem piedade).
- Nenhuma lavagem de roupas é realmente feita. Isso aqui é código, não mágica.
