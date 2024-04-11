FROM python:3.12-alpine


# Установка зависимостей для сборки (если требуются)
RUN pip install --upgrade --no-cache-dir pip

WORKDIR /School

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Запуск Django
RUN chmod +x run.sh