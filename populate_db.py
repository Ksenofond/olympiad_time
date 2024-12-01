# app/populate_db.py
from app import create_app
from app.db.database import db
from app.db.archive.models import User, Student, Result
from datetime import datetime

app = create_app()

def populate_db():
    with app.app_context():
        # Удаление всех существующих записей для чистоты
        db.drop_all()
        db.create_all()

        # Путь к фотографиям
        photo_paths = [
            'static/images/profile_pics/1/happy_cat.jpg',
            'static/images/profile_pics/2/happy_cat.jpg',
            'static/images/profile_pics/3/happy_cat.jpg',
            'static/images/profile_pics/4/happy_cat.jpg',
            'static/images/profile_pics/5/happy_cat.jpg',
        ]

        # Создание пользователей с паролем, совпадающим с email
        users = [
            User(email='ivan@example.com', phone_number='+6-900-123-45-67', photo=photo_paths[0], role='student'),
            User(email='maria@example.com', phone_number='+6-900-765-43-21', photo=photo_paths[1], role='student'),
            User(email='alexey@example.com', phone_number='+6-900-987-65-43', photo=photo_paths[2], role='student'),
            User(email='olga@example.com', phone_number='+6-900-234-56-78', photo=photo_paths[3], role='student'),
            User(email='dmitry@example.com', phone_number='+6-900-345-67-89', photo=photo_paths[4], role='student'),
        ]

        # Установка паролей, совпадающих с email
        for user in users:
            user.set_password(user.email)  # Пароль = email

        # Добавление пользователей в сессию
        db.session.add_all(users)
        db.session.commit()

        # Создание студентов
        students = [
            Student(student_name='Иван', student_surname='Иванов', student_patronymic='Иванович',
                    grade='10', email='ivan@example.com', phone_number='+6-900-123-45-67',
                    photo=photo_paths[0], bio="Пример биографии 1", user_id=users[0].id),
            Student(student_name='Мария', student_surname='Петрова', student_patronymic='Сергеевна',
                    grade='11', email='maria@example.com', phone_number='+6-900-765-43-21',
                    photo=photo_paths[1], bio="Пример биографии 2", user_id=users[1].id),
            Student(student_name='Алексей', student_surname='Сидоров', student_patronymic='Александрович',
                    grade='9', email='alexey@example.com', phone_number='+6-900-987-65-43',
                    photo=photo_paths[2], bio="Пример биографии 3", user_id=users[2].id),
            Student(student_name='Ольга', student_surname='Кузнецова', student_patronymic='Сергеевна',
                    grade='12', email='olga@example.com', phone_number='+6-900-234-56-78',
                    photo=photo_paths[3], bio="Пример биографии 4", user_id=users[3].id),
            Student(student_name='Дмитрий', student_surname='Федоров', student_patronymic='Дмитриевич',
                    grade='11', email='dmitry@example.com', phone_number='+6-900-345-67-89',
                    photo=photo_paths[4], bio="Пример биографии 5", user_id=users[4].id),
        ]

        # Добавление студентов в сессию
        db.session.add_all(students)
        db.session.commit()

        # Создание результатов
        results = [
            Result(user_id=users[0].id, score=85, olympiad_name='Олимпиада по математике', date=datetime(2024, 5, 10)),
            Result(user_id=users[1].id, score=90, olympiad_name='Олимпиада по физике', date=datetime(2024, 5, 15)),
            Result(user_id=users[2].id, score=78, olympiad_name='Олимпиада по информатике', date=datetime(2024, 5, 20)),
            Result(user_id=users[3].id, score=92, olympiad_name='Олимпиада по химии', date=datetime(2024, 6, 5)),
            Result(user_id=users[4].id, score=88, olympiad_name='Олимпиада по биологии', date=datetime(2024, 6, 10)),
        ]

        # Добавление результатов в сессию
        db.session.add_all(results)
        db.session.commit()

        print("База данных успешно заполнена начальными записями.")


if __name__ == '__main__':
    populate_db()
