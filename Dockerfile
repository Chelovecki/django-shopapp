# версия питона для использования
FROM python:3.13


# объявление перемен окружения (ENV), я говорю, что не надо использовать буферизацию. нужно, чтобы сразу же выводить логи в консоль
ENV PYTHONUNBUFFERED=1


# папка, в которой мы будем работать и где будут находиться файлы проекта
WORKDIR /app


# скачивание и установка зависимостей через poetry

RUN pip install --upgrade pip "poetry==1.8.5"
# скопировать файлы .toml и .lock  в текущую рабочую директорию (папку app)
COPY pyproject.toml poetry.lock ./
# не нужно создавать виртуальные окружения
RUN poetry config virtualenvs.create false --local
RUN poetry install


# скопирует все содержимое папки mysite внутрь проекта (не папку, но ее содержимое)
COPY mysite .


# выполнение команды для запуска сервера
CMD ['gunicorn', 'mysite.wsgi:application', '--bind', '0.0.0.0:8000']

