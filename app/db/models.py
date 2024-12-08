from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Модель пользователя
class Account(db.Model, UserMixin):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)  # Электронная почта
    phone_number = db.Column(db.String(20), nullable=True)  # Номер телефона
    photo = db.Column(db.String(256), nullable=True)  # Фото профиля
    password_hash = db.Column(db.String(256), nullable=False)  # Хеш пароля
    role = db.Column(db.String(50), nullable=False, default='student')  # Роль пользователя
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата обновления

    # Установка пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Проверка пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    def get_profile_picture(self):
        """Возвращает путь к фото профиля, если оно есть."""
        return self.photo or '/static/images/profile_pics/default_profile_pic.png'  # Путь к фото по умолчанию


# Модель студента
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)  # Внешний ключ на Account
    student_name = db.Column(db.String(150), nullable=False)  # Имя студента
    student_surname = db.Column(db.String(150), nullable=False)  # Фамилия студента
    student_patronymic = db.Column(db.String(150), nullable=True)  # Отчество студента
    grade = db.Column(db.String(50), nullable=True)  # Класс студента
    bio = db.Column(db.String(256), nullable=True)  # Биография студента

    user = db.relationship('User', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'<Student {self.student_name} {self.student_surname}>'


# Модель направления
class Direction(db.Model):
    __tablename__ = 'direction'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Название направления
    description = db.Column(db.String(256), nullable=True)  # Описание направления

    def __repr__(self):
        return f'<Direction {self.name}>'


# Модель предмета
class Subject(db.Model):
    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'), nullable=False)  # Внешний ключ на Direction
    name = db.Column(db.String(100), nullable=False)  # Название предмета
    description = db.Column(db.Text, nullable=True)  # Описание предмета
    demo_version = db.Column(db.String(256), nullable=True)  # Демо-версия предмета
    status = db.Column(db.String(50), nullable=False, default='active')  # Статус предмета

    direction = db.relationship('Direction', backref=db.backref('subjects', lazy=True))

    def __repr__(self):
        return f'<Subject {self.name}>'


# Модель олимпиады
class Olympiad(db.Model):
    __tablename__ = 'olympiad'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)  # Внешний ключ на Subject
    name = db.Column(db.String(100), nullable=False)  # Название олимпиады
    date = db.Column(db.DateTime, nullable=False)  # Дата проведения олимпиады
    description = db.Column(db.Text, nullable=True)  # Описание олимпиады
    passing_score = db.Column(db.Integer, nullable=True)  # Проходной балл
    status = db.Column(db.String(50), nullable=False, default='upcoming')  # Статус олимпиады

    subject = db.relationship('Subject', backref=db.backref('olympiads', lazy=True))

    def __repr__(self):
        return f'<Olympiad {self.name}>'


# Модель регистрации на олимпиаду
class OlympiadRegistration(db.Model):
    __tablename__ = 'olympiad_registration'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # Внешний ключ на Student
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.id'), nullable=False)  # Внешний ключ на Olympiad
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата регистрации
    status = db.Column(db.String(50), nullable=False, default='pending')  # Статус регистрации

    student = db.relationship('Student', backref=db.backref('registrations', lazy=True))
    olympiad = db.relationship('Olympiad', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        return f'<OlympiadRegistration Student ID {self.student_id} Olympiad ID {self.olympiad_id}>'


# Модель результата олимпиады
class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)  # Внешний ключ на User
    olympiad_name = db.Column(db.String(150), nullable=False)  # Название олимпиады
    score = db.Column(db.Integer, nullable=False)  # Набранные баллы
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата получения результата
    status = db.Column(db.String(50), nullable=False, default='not_checked')  # Статус результата

    user = db.relationship('User', backref=db.backref('results', lazy=True))

    def __repr__(self):
        return f'<Result {self.olympiad_name} - {self.score}>'

# Модель школы
class School(db.Model):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)              # Уникальный идентификатор
    name = db.Column(db.String(150), nullable=False)          # Название школы
    address = db.Column(db.String(256), nullable=True)        # Адрес школы
    phone_number = db.Column(db.String(50), nullable=True)    # Телефон школы
    email = db.Column(db.String(150), nullable=True)          # Электронная почта
    website = db.Column(db.String(150), nullable=True)        # Веб-сайт
    student_capacity = db.Column(db.Integer, nullable=True)   # Вместимость школы
    established_year = db.Column(db.Integer, nullable=True)   # Год основания
    description = db.Column(db.Text, nullable=True)           # Описание школы

    def __repr__(self):
        return f'<School {self.name}>'

# Модель баллов и статусов участников
class Scores(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)                  # Уникальный идентификатор
    passing_score = db.Column(db.Integer, nullable=False)         # Проходной балл
    participant_status = db.Column(db.String(50), nullable=False) # Статус участника
    # Статус участника должен быть одним из: 'Участник', 'Бронза', 'Серебро', 'Золото'
    __table_args__ = (
        db.CheckConstraint(
            participant_status.in_(['Участник', 'Бронза', 'Серебро', 'Золото']),
            name='check_participant_status'
        ),
    )

    def __repr__(self):
        return f'<Scores {self.participant_status} - {self.passing_score}>'

# Модель этапов олимпиады
class OlympiadStages(db.Model):
    __tablename__ = 'olympiad_stages'

    id = db.Column(db.Integer, primary_key=True)      # Уникальный идентификатор
    name = db.Column(db.String(100), nullable=False)  # Название этапа
    status = db.Column(db.String(50), nullable=False) # Статус этапа
    # Статус этапа должен быть одним из: 'Участник', 'Победитель', 'Финалист', 'Призёр'
    __table_args__ = (
        db.CheckConstraint(
            status.in_(['Участник', 'Победитель', 'Финалист', 'Призёр']),
            name='check_olympiad_stage_status'
        ),
    )

    def __repr__(self):
        return f'<OlympiadStages {self.name} - {self.status}>'
