# Это наш сервер. Он будет слушать команды.
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

# Создаем приложение
app = FastAPI()

# --- Это модель данных для приветствия (то, что мы будем принимать в JSON) ---
class Greeting(BaseModel):
    name: str
    mood: str = "happy"  # Если настроение не указали, то оно счастливое

# --- 1. Самый простой метод ---
@app.get("/")
async def root():
    return {"message": "Привет, юный тестировщик! Сервер работает!"}

# --- 2. Метод, который читает параметры в адресе (Query Parameters) ---
@app.get("/hello")
async def say_hello(name: str = "Аноним", age: int = 0):
    """Приветствует пользователя по имени и возрасту."""
    if age <= 0:
        return {"answer": f"Привет, {name}! Не хочешь сказать свой возраст?"}
    else:
        return {"answer": f"Привет, {name}! Тебе уже {age} лет, это круто!"}

# --- 3. Метод, который читает заголовки (Headers) ---
@app.get("/secret")
async def read_secret(secret_header: Optional[str] = Header(None)):
    """Отдает секрет, если в заголовке 'secret-header' передан пароль."""
    if secret_header == "top_secret_123":
        return {"secret": "Пароль от Wi-Fi: qwerty123"}
    elif secret_header is None:
        raise HTTPException(status_code=400, detail="Ты забыл передать заголовок secret-header!")
    else:
        raise HTTPException(status_code=403, detail="Неверный пароль! Шпион?")

# --- 4. Метод, который читает JSON тело запроса ---
@app.post("/greet")
async def greet_person(greeting: Greeting):
    """Отвечает взаимностью на присланное приветствие в формате JSON."""
    return {
        "response": f"О, привет, {greeting.name}! Рад видеть тебя в '{greeting.mood}' настроении!"
    }

# Команда для запуска (нужно написать в терминале, это не часть кода):
# uvicorn my_super_server:app --reload