from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    # Проверка, получен ли файл
    if "file" not in request.files:
        return "Файл не получен!", 400

    # Получение информации о файле
    file = request.files["file"]
    filename = secure_filename(file.filename)

    # Сохранение файла на сервере
    file.save(os.path.join("uploads", filename))

    # Отправка сообщения об успехе
    return "Файл успешно загружен!", 200

@app.route("/download/<filename>")
def download_file(filename):
    # Проверка, существует ли файл
    if not os.path.exists(os.path.join("uploads", filename)):
        return "Файл не найден!", 404

    # Отправка файла для скачивания
    return send_file(os.path.join("uploads", filename))

if __name__ == "__main__":
    app.run(debug=True)
