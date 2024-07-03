# Dockerfile (backend)
# Используем python 3.9 image
FROM python:3.9-slim

# Устанавливаем рабочий каталог
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной исходный код
COPY . .

# Открываем порт для uvicorn
EXPOSE 8000
EXPOSE 5432

# Запускаем сервер с uvicorn
CMD ["uvicorn", "scr.main:app", "--host", "0.0.0.0", "--port", "8000"]
