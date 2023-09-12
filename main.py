from typing import Optional
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TaskModel(BaseModel):
    id: int
    subject: Optional[str] = None
    context: Optional[str] = None

    def get_item(self):
        return {'id': self.id, 'subject': self.subject, 'context': self.context}
@app.get("/")
async def root():
    logger.info('Отработал GET запрос.')
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



@app.get("/show_db", response_class=HTMLResponse)
async def read_item(request: Request):
    users = [{'id': 1, 'subject': 'subject1', 'context': 'context1'},
             {'id': 2, 'subject': 'subject2', 'context': 'context2'},
             ]
    # users = {'users': users}

    return templates.TemplateResponse("show_db.html", {"request": request, "users": users})

@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request":request, "name": name})


# Запуск:
# uvicorn main:app --reload

