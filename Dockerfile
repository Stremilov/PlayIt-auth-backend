FROM python:3.11-slim


WORKDIR /app

# Копирую зависимости и устанавливаю их
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копирую весь проект
COPY . .


# Открываю порт
EXPOSE 8000

CMD ["python", "main.py"]
