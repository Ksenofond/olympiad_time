import os
from app import create_app, db
from app.db.models import Account, Student, Direction, Subject, Olympiad, OlympiadRegistration, Result, School, Scores, OlympiadStages

app = create_app()

def create_database():
    # Проверяем, существует ли база данных
    if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        with app.app_context():  # Открываем контекст приложения
            db.create_all()  # Создаём все таблицы
            print("База данных успешно создана!")

if __name__ == '__main__':
    create_database()  # Проверяем и создаём базу данных, если она не существует
    app.run(debug=True)  # Запускаем приложение
