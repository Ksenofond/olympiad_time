import json
from faker import Faker

fake = Faker()

def generate_results(count=10):
    results = []
    for i in range(count):
        result = {
            "user_id": (i % 10) + 1,               # Привяжите к существующему пользователю
            "olympiad_name": fake.word().capitalize() + " Olympiad",
            "score": fake.random_int(min=0, max=100),
            "date": fake.date_time_this_year().isoformat()
        }
        results.append(result)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    generate_results(10)
