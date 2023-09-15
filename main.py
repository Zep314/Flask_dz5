import logging
from fastapi import FastAPI, Request
from model import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/")
async def create_user(user: User):
    logger.info('Отработал POST запрос.')
    logger.info(f'{user.get_user()}')
    users.append(user)
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id < len(users):
        users[user_id] = user
        logger.info(f'Отработал PUT запрос для user_id = {user_id}.')
        logger.info(f'{user.get_user()}')
        return {"user_id": user_id, "user": user}
    else:
        logger.error(f"User {user_id} not found.")
        return {"error": "User not found."}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        del users[user_id]
    except BaseException as e:
        logger.error(f"User {user_id} not found.")
        logging.exception(e)
        return {"error": "User not found."}
    logger.info(f'Отработал DELETE запрос для user_id = {user_id}.')
    return {"user_id": user_id}


@app.get("/users/")
async def get_users():
    logger.info(f'Отработал GET запрос. Вернул всю базу.')
    return [user for user in users]


@app.get("/users/web/", response_class=HTMLResponse)
async def get_web_users(request: Request):
    return templates.TemplateResponse("show_db.html", {"request": request, "users": users})

# Запуск:
# uvicorn main:app --reload

# Windows:

# POST запросы:
# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/
# -d "{\"name\": \"Ivan\", \"email\": \"ivan@mail.ru\", \"password\": \"SuperPa$$w0rd\"}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/
# -d "{\"name\": \"Vasily\", \"email\": \"vasya@yandex.ru\", \"password\": \"MegaSecret\"}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/
# -d "{\"name\": \"Olga\", \"email\": \"olga@list.ru\", \"password\": \"C00lPar0l\"}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/
# -d "{\"name\": \"Stas\", \"email\": \"stas@gmail.com\", \"password\": \"HackMe!\"}"

# PUT запрос:
# curl -H "accept: application/json" -H "Content-Type: application/json" -X PUT http://127.0.0.1:8000/users/2
# -d "{\"name\": \"Mike\", \"email\": \"mike@nasa.com\", \"password\": \"IWantToBeleve\"}"

# DELETE запрос:
# curl -H "accept: application/json" -X DELETE http://127.0.0.1:8000/users/1

# GET запрос:
# curl -H "accept: application/json"  -H "Content-Type: application/json" -X GET http://127.0.0.1:8000/users/
