import json
from faker import Faker

fake = Faker()

def generate_olympiads(count=10):
    olympiads = []
    for i in range(count):
        olympiad = {
            "subject_id": (i % 10) + 1,  # Привяжите к существующему предмету
            "name": fake.word().capitalize() + " Olympiad",
            "date": fake.date_time_this_year().isoformat(),
            "description": fake.text(max_nb_chars=200),
            "passing_score": fake.random_int(min=50, max=100)
        }
        olympiads.append(olympiad)

    with open("olympiads.json", "w") as f:
        json.dump(olympiads, f, indent=4)

if __name__ == "__main__":
    generate_olympiads(10)
