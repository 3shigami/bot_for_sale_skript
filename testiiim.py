import requests
import os

# Определение URL-адреса Flask-сервера
SERVER_URL = "http://127.0.0.1:5000/upload"

# Выбор файла для отправки
file_path = "main.py"

# Открытие файла в бинарном режиме
with open(file_path, "rb") as file:
    # Подготовка данных для отправки
    data = {
        "file": (os.path.basename(file_path), file)
    }

    # Отправка POST-запроса на сервер
    response = requests.post(SERVER_URL, files=data)

    # Проверка статуса ответа
    if response.status_code == 200:
        print("Файл успешно отправлен!")
    else:
        print("Ошибка при отправке файла:", response.status_code)