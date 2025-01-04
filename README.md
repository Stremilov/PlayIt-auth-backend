
# PlayIT dev branch

## Как запустить проект с помощью Docker

1. **Клонируйте репозиторий:**
   ```bash
   git clone <https://github.com/Stremilov/PlayIt-auth-backend.git>
   cd <PlayIt-auth-backend.git>
   ```

2. **Создайте файл `.env`:**
   - Скопируйте содержимое файла `example.env` в новый файл с именем `.env`:
     ```bash
     cp example.env .env
     ```
   - Поменяйте значения там на другие, которые нужны вам. ОБЯЗАТЕЛЬНО СМЕНИТЕ ПАРОЛЬ В **.env** и **docker-compose.yml** файлах!

3. **Запустите Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Проверьте доступность приложения:**
   - Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).
   - Документация API: [http://localhost:8000/docs](http://localhost:8000/docs).

---

## End-Points

[![image.png](https://i.postimg.cc/W4VvRrc1/image.png)](https://postimg.cc/DSxDLSz9)