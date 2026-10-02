from enum import Enum
from fastapi import FastAPI, status, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
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

class TaskNotFoundException(Exception):
  def __init__(self, task_id: int):
    self.task_id = task_id

@app.exception_handler(TaskNotFoundException)
def task_not_found_handler(_request: Request, exc: TaskNotFoundException):
  return JSONResponse (
    status_code = status.HTTP_404_NOT_FOUND,
    content = {
      "status": "Not Found",
      "message": f"Task not found for id {exc.task_id}.",
      "data": None,
    } 
  )

def verify_jwt_token(token: str = Header(None)):
  if token == None or len(token) == 0:
    return {
      "status": "UnAuthorize",
      "message": "Token required"
    }
  
  if token != 'mysecrettoken':
    return {
      "status": "UnAuthorize",
      "message": "Invalid Token"
    }

  return {
    "status": "Ok",
    "message": "Valid Token"
  }


def testing_depends():
  return {
    "message-url": "https://www.google.com",
  }

@app.middleware('http')
async def verify_jwt_token(request:Request, call_next):
  paths = request.url.path
  if paths in ['/private/health']:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
      return JSONResponse(
        status_code=401,
        content={
          "success": False,
          "message": "Invalid header or missing header"
        }
      )
    request.state.token = auth_header.split(" ")[1]
    response = await call_next(request)
    return response
  else:
    return await call_next(request)

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
@app.get('/todo', status_code=status.HTTP_200_OK)
def get_all_task(status: TaskStatus = None, data = Depends(verify_jwt_token)):
  if data["status"] != 'Ok':
    raise HTTPException(
      status_code = 401,
      detail=data
    )

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
def get_task(task_id: int, data = Depends(testing_depends)):
  filtered_task = [t for t in tasks if t["id"] == task_id]

  if len(filtered_task) == 0:
    raise TaskNotFoundException(task_id)

  return {
    "status": "Ok",
    "message": "Task get success.",
    "data": filtered_task,
    "depends": data,
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


@app.get('/private/health')
def private_health(request: Request):
  return {
    "status": "Ok",
    "message": "Server health is ok",
    "data": request.state.token,
  }