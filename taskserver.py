import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Менеджер задач API")

# ============= МОДЕЛИ =============

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: str

# ============= ХРАНИЛИЩЕ =============

tasks = {}
next_id = 0  # счетчик для генерации ID

# ============= API =============

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """Создает новую задачу"""
    global next_id
    
    task_id = next_id
    next_id += 1
    
    tasks[task_id] = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return tasks[task_id]

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(completed: Optional[bool] = None):
    """Возвращает список задач (можно фильтровать по статусу)"""
    result = list(tasks.values())
    
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    
    # Сортируем по ID (новые сверху)
    result.sort(key=lambda x: x["id"], reverse=True)
    
    return result

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Возвращает задачу по ID"""
    if task_id not in tasks:
        raise HTTPException(404, "Задача не найдена")
    return tasks[task_id]

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """Обновляет задачу"""
    if task_id not in tasks:
        raise HTTPException(404, "Задача не найдена")
    
    if task_update.title is not None:
        tasks[task_id]["title"] = task_update.title
    
    if task_update.description is not None:
        tasks[task_id]["description"] = task_update.description
    
    if task_update.completed is not None:
        tasks[task_id]["completed"] = task_update.completed
    
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    if task_id not in tasks:
        raise HTTPException(404, "Задача не найдена")
    
    del tasks[task_id]
    return {"message": "Задача удалена"}

@app.get("/stats")
def get_stats():
    """Возвращает статистику по задачам"""
    if not tasks:
        return {"message": "Нет задач"}
    
    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["completed"])
    active = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "active": active,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
    }

if __name__ == "__main__":
    uvicorn.run("taskserver:app", host="127.0.0.1", port=8000, reload=True)