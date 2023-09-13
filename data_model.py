from sqlalchemy import SQLAlchemy
from datetime import datetime
import databases



class User(db.Model):
    """
    Класс USer - описываем одну запись о пользователе в базе данных
    """
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120))
    context = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, subject='{self.subject}', context='{self.context}', " \
               f"is_active='{self.is_active}', created_at={self.created_at.strftime('%m/%d/%Y, %H:%M:%S')})>"
