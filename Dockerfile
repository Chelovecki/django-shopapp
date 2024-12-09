# версия питона для использования
FROM python:3.11

# объявление перемен окружения (ENV), я говорю, что не надо использовать буферизацию. нужно, чтобы сразу же выводить логи в консоль
ENV PYTHONUNBUFFERED=1
# папка, в которой мы будем работать и где будут находиться файлы проекта
WORKDIR /app

# скопировать данные из файла requirements.txt и сохранить в докер в файле под названием requirements.txt
COPY requirements.txt requirements.txt

# запуск команды для обновления pip и скачивания всех зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# скопирует все содержимое папки mysite внутрь проекта (не папку, но ее содержимое)
COPY mysite .

