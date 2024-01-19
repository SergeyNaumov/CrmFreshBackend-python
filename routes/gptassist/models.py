from pydantic import BaseModel

# Модели для запросов
class RequestGPT(BaseModel):
  config: str
  engine: int
  request: str


# Запрос к GPT
class RequestTask(BaseModel):
  engine: int
  temperature: float
  sys_text: str
  ask: str

class DaemonResult(BaseModel):
  status: int
  task_id: str
  question: str