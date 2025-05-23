
# PlayIT main branch

## Использованные технологии
```
- Python
- FastAPI
- FastAPI Users
- Sqlalchemy
- PostgreSQL
- Docker
- Grafana
- Loki
- Prometheus
- GitHub Actions
```

## Как запустить проект с помощью Docker

### 1. Клонируйте репозиторий:
```bash
git clone <https://github.com/Stremilov/PlayIt-auth-backend.git>
cd <PlayIt-auth-backend.git>
```

### 2. Создайте файл `.env`:
- Скопируйте содержимое файла `example.env` в новый файл с именем `.env`:
  ```bash
  cp example.env .env
  ```
- Измените значения переменных на те, которые вам нужны. **Обязательно смените пароль** в файлах `.env` и `docker-compose.yml`!

### 3. Установите плагин Loki для логирования:
Чтобы проект мог корректно работать с логированием через Grafana Loki, необходимо установить плагин Loki в Docker:
```bash
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

#### Зачем нужен плагин Loki?
Плагин Loki позволяет контейнерам отправлять логи в систему логирования Grafana Loki. Это упрощает мониторинг, позволяет централизованно хранить логи и анализировать их через Grafana.

### 4. Поднимите сеть `skynet`:
Проект использует внешнюю Docker-сеть `skynet`, чтобы обеспечить взаимодействие между сервисами. Если она ещё не создана, выполните:
```bash
docker network create skynet
```

#### Зачем нужна сеть `skynet`?
Docker-сеть `skynet` позволяет контейнерам проекта (например, базе данных и приложению) общаться друг с другом по именам сервисов (`db`, `db_test`, и т.д.), а также отделяет их от других проектов для предотвращения конфликтов.

### 5. Запустите Docker Compose:
```bash
docker-compose up --build
```

### 6. Проверьте доступность приложения:
- Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).
- Документация API: [http://localhost:8000/docs](http://localhost:8000/docs).




## Инструкция по запуску тестов

### Как запустить тесты из-под Docker
1. **Откройте контейнер приложения в интерактивном режиме:**
   ```bash
   docker exec -it playit-auth-backend bash
   ```

2. **Запустите тесты внутри контейнера:**
   ```bash
   pytest
   ```

3. **Для проверки покрытия кода тестами:**
   ```bash
   pytest --cov
   ```
   или
   ```bash
   pytest --cov=src
   ```

4. **Выход из контейнера:**
   После завершения работы можно выйти из контейнера, набрав:
   ```bash
   exit
   ```
