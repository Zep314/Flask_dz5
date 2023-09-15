"""
Модуль для хранения модели данных
"""
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    Класс для хранения элемента данных с функциями проверки полей данных
    """
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    def get_user(self):
        return {'name': self.name, 'email': self.email, 'password': self.password}
