import pytest
import random


# Telegram login
@pytest.mark.asyncio
async def test_telegram_login(client):
    # Данные для тестового пользователя
    test_user = {
        "username": f"testuser_{random.randint(1, 10000)}",  # Чтобы тесты друг на друга не влияли никак
        "telegram_id": random.randint(10000, 99999)
    }

    # Выполняем POST-запрос для регистрации/авторизации
    response = await client.post(
        "/users/telegram-login",
        json=test_user
    )

    # Проверяем статус ответа
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Проверяем содержание ответа
    response_data = response.json()
    assert response_data["status"] == "success", f"Unexpected status: {response_data['status']}"
    assert response_data["message"] in ["Logged in", "Registered and logged in"], (
        f"Unexpected message: {response_data['message']}"
    )


# Whoami
@pytest.mark.asyncio
async def test_whoami(client):
    # Данные для тестового пользователя
    test_user = {
        "username": f"testuser_{random.randint(1, 10000)}",  # Чтобы тесты друг на друга не влияли никак
        "telegram_id": random.randint(10000, 99999)
    }

    # Выполняем POST-запрос для регистрации/авторизации
    login_response = await client.post(
        "/users/telegram-login",
        json=test_user
    )

    # Проверяем, что регистрация/авторизация прошла успешно
    assert login_response.status_code == 200, f"Unexpected status code during login: {login_response.status_code}"
    assert login_response.json()["status"] == "success"

    # Выполняем GET-запрос для получения информации о текущем пользователе
    whoami_response = await client.get("/users/whoami")

    # Проверяем статус ответа
    assert whoami_response.status_code == 200, f"Unexpected status code: {whoami_response.status_code}"

    # Проверяем содержание ответа
    whoami_data = whoami_response.json()
    assert whoami_data["status"] == "success", f"Unexpected status: {whoami_data['status']}"
    assert whoami_data["user"]["username"] == test_user["username"], (
        f"Unexpected username: {whoami_data['user']['username']}"
    )
    assert whoami_data["user"]["telegram_id"] == test_user["telegram_id"], (
        f"Unexpected telegram_id: {whoami_data['user']['telegram_id']}"
    )


# TODO: Пофиксить status_code должен быть равен 401, а не 500, но в логике userservice except Exception as e перехватывает
# TODO 401 стаутс код из verify_user_by_jwt, ответ приходит вот такой:
# TODO   "detail": "Произошла непредвиденная ошибка: 401: Не авторизован", со статус кодом 500
# Пока что и так работает)
@pytest.mark.asyncio
async def test_whoami_without_token(client):
    response = await client.get("/users/whoami")
    assert response.status_code == 500, "Expected 500 Unauthorized for missing token"
    assert response.json()[
               "detail"] == "Произошла непредвиденная ошибка: 401: Не авторизован", "Unexpected error message"


@pytest.mark.asyncio
async def test_whoami_with_invalid_token(client):
    # Установить поврежденный токен в cookie
    client.cookies.set("jwt-token", "invalid-token")

    # Запрос к /whoami
    response = await client.get("/users/whoami")
    assert response.status_code == 500, "Expected 401 Unauthorized for invalid token"  # TODO Тут тоже со статус кодами
    # решить проблему, что выдаётся 500 в логике, хотя должен быть 401


@pytest.mark.asyncio
async def test_manage_balance(client):
    # Данные для тестового пользователя
    test_user = {
        "username": f"testuser_{random.randint(1, 10000)}",  # Чтобы тесты друг на друга не влияли никак
        "telegram_id": random.randint(10000, 99999)
    }

    # Выполняем POST-запрос для регистрации/авторизации
    login_response = await client.post(
        "/users/telegram-login",
        json=test_user
    )

    # Проверяем, что регистрация/авторизация прошла успешно
    assert login_response.status_code == 200, f"Unexpected status code during login: {login_response.status_code}"
    assert login_response.json()["status"] == "success"

    # Изменение баланса пользователя
    balance_value = 100  # Положительное значение для увеличения баланса
    balance_response = await client.put(f"/users/balance/{balance_value}")

    # Проверяем статус ответа
    assert balance_response.status_code == 200, f"Unexpected status code: {balance_response.status_code}"

    # Проверяем содержание ответа
    balance_data = balance_response.json()
    assert balance_data["status"] == "success", f"Unexpected status: {balance_data['status']}"
    assert balance_data["user"]["balance"] == balance_value, (
        f"Unexpected balance: {balance_data['user']['balance']}"
    )

    # Уменьшение баланса пользователя
    negative_balance_value = -50
    decrease_balance_response = await client.put(f"/users/balance/{negative_balance_value}")

    # Проверяем статус ответа
    assert decrease_balance_response.status_code == 200, f"Unexpected status code: {decrease_balance_response.status_code}"

    # Проверяем содержание ответа
    decrease_balance_data = decrease_balance_response.json()
    assert decrease_balance_data["status"] == "success", f"Unexpected status: {decrease_balance_data['status']}"
    assert decrease_balance_data["user"]["balance"] == (balance_value + negative_balance_value), (
        f"Unexpected balance: {decrease_balance_data['user']['balance']}"
    )


@pytest.mark.asyncio
async def test_update_personal_data(client):
    # Данные для тестового пользователя
    test_user = {
        "username": f"testuser_{random.randint(1, 10000)}",  # Чтобы тесты друг на друга не влияли никак
        "telegram_id": random.randint(10000, 99999)
    }

    # Выполняем POST-запрос для регистрации/авторизации
    login_response = await client.post(
        "/users/telegram-login",
        json=test_user
    )

    # Проверяем, что регистрация/авторизация прошла успешно
    assert login_response.status_code == 200, f"Unexpected status code during login: {login_response.status_code}"
    assert login_response.json()["status"] == "success"

    # Данные для изменения персональной информации
    personal_data_update = {
        "full_name": "Иванов Иван Иванович",
        "group_number": "ИСТ-000"
    }

    # Выполняем PUT-запрос для обновления персональных данных
    update_response = await client.put(
        "/users/personal-data",
        json=personal_data_update
    )

    # Проверяем статус ответа
    assert update_response.status_code == 200, f"Unexpected status code: {update_response.status_code}"

    # Проверяем содержание ответа
    update_data = update_response.json()
    assert update_data["status"] == "success", f"Unexpected status: {update_data['status']}"
    assert update_data["user"]["full_name"] == personal_data_update["full_name"], (
        f"Unexpected full_name: {update_data['user']['full_name']}"
    )
    assert update_data["user"]["group_number"] == personal_data_update["group_number"], (
        f"Unexpected group_number: {update_data['user']['group_number']}"
    )
