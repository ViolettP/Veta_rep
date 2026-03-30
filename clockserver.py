import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta

app = FastAPI(title="Лавка часов")



class BaseClock:
    def __init__(self, id: str, name: str, clock_type: str, initial_time: str):
        self.id = id
        self.name = name
        self.type = clock_type
        self.time = datetime.strptime(initial_time, "%H:%M:%S")
        self.ticks = 0
    
    def get_time(self):
        return self.time.strftime("%H:%M:%S")

class NormalClock(BaseClock):
    def tick(self):
        old = self.get_time()
        self.time += timedelta(seconds=1)
        self.ticks += 1
        return old, self.get_time()

class ReverseClock(BaseClock):
    def tick(self):
        old = self.get_time()
        self.time -= timedelta(seconds=1)
        self.ticks += 1
        return old, self.get_time()

class InvisibleClock(BaseClock):
    """Часы-невидимки - никогда не показывают цифры 3 и 7"""
    
    def _has_forbidden_digits(self, time_str: str) -> bool:
        """Проверяет, содержит ли время цифры 3 или 7"""
        return '3' in time_str or '7' in time_str
    
    def tick(self):
        old = self.get_time()       
        self.time += timedelta(seconds=1)
        while self._has_forbidden_digits(self.get_time()):
            self.time += timedelta(seconds=1)
        
        self.ticks += 1
        return old, self.get_time()



clocks = {
    "1": NormalClock("1", "Обычные часы", "normal", "12:00:00"),
    "2": ReverseClock("2", "Часы-наоборот", "reverse", "12:00:00"),
    "3": InvisibleClock("3", "Часы-невидимки", "invisible", "12:00:00")
}



@app.get("/clocks")
def get_clocks():
    """Все часы"""
    return [{"id": c.id, "name": c.name, "type": c.type, "time": c.get_time(), "ticks": c.ticks} 
            for c in clocks.values()]

@app.get("/clocks/{clock_id}")
def get_clock(clock_id: str):
    """Получить часы по ID"""
    if clock_id not in clocks:
        raise HTTPException(404, "Часы не найдены")
    
    clock = clocks[clock_id]
    return {"id": clock.id, "name": clock.name, "type": clock.type, "time": clock.get_time(), "ticks": clock.ticks}

@app.post("/clocks/{clock_id}/tick")
def tick_clock(clock_id: str):
    """Сделать тик"""
    if clock_id not in clocks:
        raise HTTPException(404, "Часы не найдены")
    
    clock = clocks[clock_id]
    old_time, new_time = clock.tick()
    
    return {
        "clock_id": clock.id,
        "clock_name": clock.name,
        "from": old_time,
        "to": new_time,
        "ticks": clock.ticks
    }

if __name__ == "__main__":
    uvicorn.run("myserver:app", host="127.0.0.1", port=8000, reload=True)