from faker import Faker
from datetime import timedelta
import random

fake = Faker(locale='ru_RU')

def generate_fake_user(min_age=18, max_age=70, registration_years=5):
    """
    Генерирует фейковый профиль пользователя.

    :param min_age: минимальный возраст пользователя
    :param max_age: максимальный возраст пользователя
    :param registration_years: максимальное количество лет назад для даты регистрации
    :return: словарь с данными пользователя
    """
    # Генерация даты рождения и даты регистрации
    birthday = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
    registration_at = fake.date_time_between(start_date=f"-{registration_years}y", end_date="now")

    # Генерация фейкового профиля пользователя
    fake_user = {
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'middle_name': fake.middle_name(),
    'phone_number': fake.phone_number(),
    'email': fake.email(),

    # Генерация адресных данных с логической структурой
    'address': {
    'country': fake.country(),
    'country_code': fake.country_code(),
    'region': fake.region(),
    'city': fake.city(),
    'street_address': fake.street_address(),
    'postcode': fake.postcode(),
    },

    # Дополнительные сведения о пользователе
    'occupation': fake.job(),
    'company': fake.company(),
    'work_phone': fake.phone_number(),
    'marital_status': random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
    'website': fake.url(),

    # Даты
    'registration_at': registration_at,
    'birthday': birthday,

    # Профиль в социальных сетях и банковские реквизиты (при необходимости)
    'social_profile': fake.url(),
    'credit_card': {
    'number': fake.credit_card_number(),
    'provider': fake.credit_card_provider(),
    'expiration_date': fake.credit_card_expire(),
        }
    }
    return fake_user

# Пример использования
fake_user = generate_fake_user()
print(fake_user)