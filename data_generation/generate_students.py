import json
from faker import Faker
import random

fake = Faker()

def generate_students(count=10):
    students = []
    for i in range(count):
        student = {
            "user_id": i + 1,  # Укажите корректный user_id
            "student_name": fake.first_name(),
            "student_surname": fake.last_name(),
            "student_patronymic": fake.first_name(),
            "grade": random.choice(["7", "8", "9", "10", "11"]),
            "bio": fake.text(max_nb_chars=200)
        }
        students.append(student)

    with open("json/students.json", "w") as f:
        json.dump(students, f, indent=4)

if __name__ == "__main__":
    generate_students(10)
