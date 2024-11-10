import json
from faker import Faker
from werkzeug.security import generate_password_hash

fake = Faker()

def generate_users(count=10):
    users = []
    for _ in range(count):
        user = {
            "email": fake.unique.email(),
            "phone_number": fake.phone_number(),
            "photo": fake.image_url(),
            "password_hash": generate_password_hash(fake.password()),
            "role": fake.random_element(elements=("student", "admin")),
            "created_at": fake.date_time_this_year().isoformat()
        }
        users.append(user)

    # Запись данных в JSON
    with open("json/users.json", "w") as f:
        json.dump(users, f, indent=4)

if __name__ == "__main__":
    generate_users(10)
