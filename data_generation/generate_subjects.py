import json
from faker import Faker

fake = Faker()

# Определим категории и предметы
categories = {
    "Естественные науки": [
        "Математика", "Астрономия", "Биология", "География", "Экология", "Физика", "Химия"
    ],
    "Общественные науки": [
        "Экономика", "Обществознание", "Право", "ОБЖ (Основы безопасности жизнедеятельности)"
    ],
    "Гуманитарные науки": [
        "Русский язык", "Литература", "Английский язык", "Испанский язык",
        "Китайский язык", "Немецкий язык", "Французский язык", "Искусство"
    ],
    "Технические науки": [
        "Информатика", "Технология"
    ],
    "Спортивное направление": [
        "Физическая культура"
    ]
}

# Словарь с описаниями предметов
subject_descriptions = {
    "Математика": "Математика — это наука о числах, формах и их взаимосвязях, изучающая закономерности природы и общества.",
    "Астрономия": "Астрономия изучает небесные тела, их движение и взаимодействие, а также происхождение и развитие Вселенной.",
    "Биология": "Биология занимается изучением жизни, живых существ и их взаимодействия с окружающей средой.",
    "География": "География изучает землю, природные и социально-экономические явления, а также их распределение по планете.",
    "Экология": "Экология исследует взаимодействие организмов с окружающей средой, а также влияние человеческой деятельности на природу.",
    "Физика": "Физика — это наука, исследующая основные законы природы, включая движение, энергию и силы.",
    "Химия": "Химия изучает вещества, их состав, свойства и превращения, а также взаимодействие атомов и молекул.",
    "Экономика": "Экономика изучает производство, распределение и потребление товаров и услуг, а также управление ресурсами.",
    "Обществознание": "Обществознание включает в себя изучение общества, его институтов, законов и процессов социальной жизни.",
    "Право": "Право — это система норм и правил, регулирующих отношения между людьми и организациями в обществе.",
    "ОБЖ": "Основы безопасности жизнедеятельности изучают меры предосторожности для защиты человека от различных опасностей.",
    "Русский язык": "Русский язык изучает правила построения слов и предложений, а также грамматику и орфографию.",
    "Литература": "Литература охватывает художественные произведения, изучая их тематику, жанры и стили.",
    "Английский язык": "Английский язык — международный язык общения, используемый для общения в бизнесе, науке и повседневной жизни.",
    "Испанский язык": "Испанский язык широко распространён в мире, изучение которого позволяет общаться с носителями в странах Латинской Америки и Испании.",
    "Китайский язык": "Китайский язык — один из самых древних и сложных языков мира, на котором говорят в Китае и некоторых других странах.",
    "Немецкий язык": "Немецкий язык используется в Германии, Австрии и Швейцарии, и является важным для бизнеса и науки.",
    "Французский язык": "Французский язык является официальным языком Франции и используется во многих странах мира.",
    "Искусство": "Искусство включает в себя изучение различных видов творчества: живопись, музыка, театральное искусство и многое другое.",
    "Информатика": "Информатика изучает компьютеры, программирование, обработку и хранение информации, а также использование технологий в различных сферах.",
    "Технология": "Технология охватывает процессы создания, производства и использования различных продуктов и услуг.",
    "Физическая культура": "Физическая культура включает в себя занятия спортом, физической активностью и формирование здорового образа жизни."
}


def generate_subjects():
    subjects = []
    direction_id = 1  # Уникальный идентификатор для направления

    for direction_name, subjects_list in categories.items():
        for subject_name in subjects_list:
            subject = {
                "direction_id": direction_id,  # Привязываем предмет к текущему направлению
                "name": subject_name,
                "description": subject_descriptions.get(subject_name, "Описание не найдено."),
                "demo_version": fake.url()  # Генерация ссылки на демо-версию
            }
            subjects.append(subject)
        direction_id += 1

    # Запись данных в JSON-файл
    with open("json/subjects.json", "w", encoding="utf-8") as f:
        json.dump(subjects, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    generate_subjects()
