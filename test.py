from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
import secrets
from fastapi.responses import HTMLResponse
from typing import Dict
from pydantic import BaseModel, PositiveInt
from enum import Enum


class UserData(BaseModel):
    name: str
    age: PositiveInt


user_data = {}


app = FastAPI()


@app.post("/api/save_user")
def api_save_user(data: UserData):
    user_data[data.name] = data.age


@app.post("/save_user")
def save_user(name=Form(), age=Form()):
    api_save_user(UserData(name=name, age=age))
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)


@app.get("/users")
def get_users():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Here are all users if any</h1>
            <div>{}</div>
            <a href="/add_user">Add User</a>
        </body>
    </html>
    """.format(
        ", ".join(user_data.keys())
    )
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/add_user")
def add_user():
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <form action="/save_user" method="post">
            <div class="form-example">
                <label for="name">Enter your name: </label>
                <input type="text" name="name" id="name" required>
            </div>
            <div class="form-example">
                <label for="age">Enter your age: </label>
                <input type="text" name="age" id="age" required>
            </div>
            <div class="form-example">
                <input type="submit" value="Subscribe!">
            </div>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# Задание №3
# 📌 Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для добавления нового пользователя (метод POST).
# 📌 Реализуйте валидацию данных запроса и ответа.

# Задание №4
# 📌 Создать API для обновления информации о пользователе в базе данных.
# Приложение должно иметь возможность принимать PUT запросы с данными
# пользователей и обновлять их в базе данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для обновления информации о пользователе (метод PUT).
# 📌 Реализуйте валидацию данных запроса и ответа.

# Задание №5
# 📌 Создать API для удаления информации о пользователе из базы данных.
# Приложение должно иметь возможность принимать DELETE запросы и
# удалять информацию о пользователе из базы данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для удаления информации о пользователе (метод DELETE).
# 📌 Реализуйте проверку наличия пользователя в списке и удаление его из
# списка.

# Задание №6
# 📌 Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# 📌 Создайте маршрут для отображения списка пользователей (метод GET).
# 📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.