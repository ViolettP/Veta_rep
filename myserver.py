from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Модель для JSON данных
class Item(BaseModel):
    name: str
    value: int = 0

# 1. Просто проверка
@app.get("/")
def root():
    return {"message": "ok"}

# 2. Query параметры
@app.get("/query")
def query_params(name: str = "никто", num: int = 0):
    return {
        "name": name,
        "num": num
    }

# 3. Заголовки
@app.get("/header")
def header_params(x_token: Optional[str] = Header(None)):
    if x_token == "123":
        return {"ok": True}
    return {"ok": False}

# 4. JSON тело
@app.post("/json")
def json_body(item: Item):
    return {
        "received_name": item.name,
        "received_value": item.value
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)