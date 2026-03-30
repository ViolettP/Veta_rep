from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="HTML Тег-генератор")


class TagType(str, Enum):
    """Доступные типы тегов"""
    DIV = "div"
    I = "i"
    H1 = "h1"

class TagRequest(BaseModel):
    """Модель для валидации входящих данных"""
    text: str
    tags: List[TagType]



class HTMLBuilder:
    def __init__(self, text: str = ""):
        self.text = text
        self.tags = []
    
    def div(self):
        self.tags.append("div")
        return self
    
    def i(self):
        self.tags.append("i")
        return self
    
    def h1(self):
        self.tags.append("h1")
        return self
    
    def build(self) -> str:
        if not self.tags:
            return self.text
        
        result = self.text
        for tag in reversed(self.tags):
            result = f"<{tag}>{result}</{tag}>"
        return result


@app.post("/build")
def build_html(request: TagRequest):
    """Создает HTML с тегами div, i, h1"""
    builder = HTMLBuilder(request.text)
    
    for tag in request.tags:
        if tag == TagType.DIV:
            builder.div()
        elif tag == TagType.I:
            builder.i()
        elif tag == TagType.H1:
            builder.h1()
    
    return {"html": builder.build()}

if __name__ == "__main__":
    uvicorn.run("htmltagserver:app", host="127.0.0.1", port=8000, reload=True)