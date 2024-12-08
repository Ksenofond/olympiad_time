from app import create_app

def create_database():
    app = create_app()  # Создаём экземпляр приложения
    with app.app_context():  # Запускаем контекст приложения
        from app.db import init_db  # Импортируем функцию для инициализации базы данных
        init_db(app)  # Инициализируем базу данных

if __name__ == "__main__":
    create_database()  # Запускаем процесс создания базы данных
