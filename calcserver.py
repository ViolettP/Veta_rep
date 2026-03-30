from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Калькулятор API")


class CalculateRequest(BaseModel):
    a: float
    b: float
    operation: str  # add, subtract, multiply, divide

class CalculateResponse(BaseModel):
    result: float
    operation: str
    expression: str

class HistoryItem(BaseModel):
    expression: str
    result: float
    timestamp: str


history = []


@app.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest):
    """Выполняет арифметическую операцию"""
    
    if request.operation == "+":
        result = request.a + request.b
        expression = f"{request.a} + {request.b} = {result}"
    
    elif request.operation == "-":
        result = request.a - request.b
        expression = f"{request.a} - {request.b} = {result}"
    
    elif request.operation == "*":
        result = request.a * request.b
        expression = f"{request.a} * {request.b} = {result}"
    
    elif request.operation == "/":
        if request.b == 0:
            raise HTTPException(400, "На ноль делить нельзя!")
        result = request.a / request.b
        expression = f"{request.a} / {request.b} = {result}"
    
    else:
        raise HTTPException(400, "Неизвестная операция")
    
    # Сохраняем в историю
    history.append(HistoryItem(
        expression=expression,
        result=result,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    return CalculateResponse(
        result=result,
        operation=request.operation,
        expression=expression
    )

@app.get("/history", response_model=List[HistoryItem])
def get_history(limit: Optional[int] = None):
    """Возвращает историю вычислений"""
    if limit:
        return history[-limit:]
    return history

@app.delete("/history")
def clear_history():
    """Очищает историю"""
    history.clear()
    return {"message": "История очищена"}


if __name__ == "__main__":
    uvicorn.run("calcserver:app", host="127.0.0.1", port=8000, reload=True)