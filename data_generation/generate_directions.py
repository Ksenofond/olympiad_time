import json
from app import app, db
from models import Direction

def generate_directions(count=5):
    # Список направлений и их описаний
    directions_data = {
        "Естественные науки": "Естественные науки изучают явления природы и законы, которые управляют окружающим миром. Это направления, связанные с изучением физического мира, включая биологические, химические, физические и географические процессы.",
        "Общественные науки": "Общественные науки занимаются изучением общества, социальных процессов, а также культурных, экономических и политических явлений, влияющих на развитие социума.",
        "Гуманитарные науки": "Гуманитарные науки направлены на изучение человека, его культуры, языка, истории и искусства. Эти науки помогают понять культуру, мораль и философию человека.",
        "Технические науки": "Технические науки связаны с созданием новых технологий, изучением инженерных решений и применением научных знаний для улучшения качества жизни. Они включают в себя инженерию, информатику и другие дисциплины.",
        "Спортивное направление": "Спортивное направление охватывает физическую культуру и спорт, изучая физическую активность, спортивные дисциплины и методы улучшения здоровья и физической формы."
    }

    # Создание направлений и добавление их в базу данных
    for direction_name, description in directions_data.items():
        # Проверяем, существует ли направление с таким именем
        existing_direction = Direction.query.filter_by(name=direction_name).first()
        if not existing_direction:
            direction = Direction(name=direction_name, description=description)
            db.session.add(direction)

    # Сохраняем изменения в базе данных
    db.session.commit()

    # Запись в файл JSON (для сохранения)
    directions = [{"name": direction.name, "description": direction.description} for direction in Direction.query.all()]
    with open("json/directions.json", "w", encoding="utf-8") as f:
        json.dump(directions, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    with app.app_context():
        generate_directions()
