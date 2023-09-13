import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from datetime import datetime
import starlette.status as status
import databases
import sqlalchemy
from typing import Annotated, List
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILENAME = 'my_database.db'
DATABASE_URL = f"sqlite:///{DB_FILENAME}"
database = databases.Database(DATABASE_URL) #, connect_args={"check_same_thread": False}
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("subject", sqlalchemy.String(32)),
    sqlalchemy.Column("context", sqlalchemy.String(128)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)


class TaskIn(BaseModel):
    subject: str = Field(title='Subject', description='Subject of task', max_len=32)
    context: str = Field(title='Context', description='Context of task', max_len=255)
    is_active: bool = Field(title='Is active', description='True, if record is active, otherwise is false',
                            default=True)
    created_at: datetime = Field(title='Creation time', description='Date & time of creation', default=datetime.utcnow)


class Task(BaseModel):
    id: int
    subject: str = Field(title='Subject', description='Subject of task', max_len=32)
    context: str = Field(title='Context', description='Context of task', max_len=255)
    is_active: bool = Field(title='Is active', description='True, if record is active, otherwise is false',
                            default=True)
    created_at: datetime = Field(title='Creation time', description='Date & time of creation', default=datetime.utcnow)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return RedirectResponse("/tasks")


@app.get("/tasks", response_class=HTMLResponse)
async def read_item(request: Request):
    all_tasks1 = await database.fetch_all(tasks.select())
    all_tasks = [{'id': task[0], 'subject': task[1], 'context': task[2]} for task in all_tasks1]
#    logger.info(all_tasks1)
    return templates.TemplateResponse("show_db.html", {"request": request, "tasks": all_tasks})


@app.get("/item", response_class=HTMLResponse)
async def item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.post("/tasks")
async def add_task(subject: Annotated[str, Form()], context: Annotated[str, Form()]):
    await api_add_task(TaskIn(subject=subject,context=context))
    return RedirectResponse("/tasks", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get

@app.post("/tasks/delete")
async def delete_task(id: Annotated[int, Form()]):
    #await api_delete_task(id)
    logger.info('try to delete')
    x = requests.delete(f'http://127.0.0.1:8000/api/tasks/{id}')
    logger.info(f'deleted {x=}')
    return RedirectResponse("/tasks", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get

@app.post("/api/tasks")
async def api_add_task(task: TaskIn):
    query = tasks.insert().values(subject=task.subject, context=task.context)
    await database.execute(query)
    logger.info('Task added!')



@app.delete("/api/tasks/{task_id}")
async def api_delete_task(task_id: int):
    logger.info(f'Task #{task_id} deleted')
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task #{task_id} deleted'}


@app.get("/items/{task_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



# Запуск:
# uvicorn main:app --reload
