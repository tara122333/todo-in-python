from enum import Enum
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [{
  "id": 1,
  "title": "A",
  "description": "sdfsd sdfio sdm jsndvl",
  "status": 'active'
},
{
  "id": 2,
  "title": "B",
  "description": "sdfsdsdvs oieir sd",
  "status": 'in_active',
},
{
  "id": 3,
  "title": "C",
  "description": "sdsdvsdv wsdfs fsd",
  "status": 'in_progress',
},
{
  "id": 4,
  "title": "D",
  "description": "sdfs sds d",
  "status": 'completed',
}]

class TaskStatus(str, Enum):
  ACTIVE = 'active'
  IN_ACTIVE = 'in_active'
  COMPLETED = 'completed'
  IN_PROGRESS = 'in_progress'

class Task(BaseModel):
  id: int
  title: str
  description: str
  status: TaskStatus

class TaskResponse(BaseModel):
  title: str
  description: str
  status: TaskStatus

class StandardRes(BaseModel):
  status: str
  message: str
  data: list[TaskResponse] or None = None

@app.get("/", status_code=status.HTTP_200_OK)
def server():
  return {
    "status": "Ok",
    "message": "Server running successfully"
  }

@app.get('/health', status_code=status.HTTP_200_OK)
def server_health():
  return {
    "status": "Ok",
    "message": "Server health is ok"
  }

# Todo application
@app.get('/todo', response_model = StandardRes, status_code=status.HTTP_200_OK)
def get_all_task(status: TaskStatus = None):
  if status == None:
    return {
      "status": "Ok",
      "message": "Task get success.",
      "data": tasks,
    }

  filtered_tasks = [t for t in tasks if t.status == status]
  return {
    "status": "Ok",
    "message": "Task get success.",
    "data": filtered_tasks,
  }

@app.get('/todo/{task_id}')
def get_task(task_id: int):
  filtered_task = [t for t in tasks if t["id"] == task_id]

  if len(filtered_task) == 0:
    raise HTTPException (
      status_code=status.HTTP_404_NOT_FOUND,
      detail="data not found",
    )

  return {
    "status": "Ok",
    "message": "Task get success.",
    "data": filtered_task,
  }

@app.post('/todo', status_code = status.HTTP_201_CREATED)
def create_task(task: Task):
  tasks.append(task)
  return {
    "status": "Ok",
    "message": "Task create success.",
    "data": task,
  }


@app.delete('/todo/{task_id}', response_model = StandardRes, status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
  for index, task in enumerate(tasks):
    if task.id == task_id:
      tasks.pop(index)
      return {
        "status": "Ok",
        "message": "Task delete success",
      }
  return {
    "status": "Failed",
    "message": "Task not deleted. Task not found..",
  }

@app.put('/todo/{task_id}', response_model = StandardRes, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: Task):
  for index, task in enumerate(tasks):
    if task.id == task_id:
      tasks[index] = task
      return {
        "status": "Ok",
        "message": "Task update success",
      }
  return {
    "status": "Failed",
    "message": "Task not found. Task not updated.",
  }
