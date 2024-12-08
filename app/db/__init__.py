# app/db/__init__.py
from app.db.database import db

def init_db(app):
    """Инициализация базы данных и создание таблиц."""
    with app.app_context():
        db.create_all()  # Создает все таблицы, если они не существуют
        print("База данных успешно создана")
