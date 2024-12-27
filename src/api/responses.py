# Для эндпоинта /users/telegram-login в src.api.users
telegram_login_responses = {
    200: {
        "description": "Успешная авторизация или регистрация",
        "content": {
            "application/json": {
                "examples": {
                    "logged_in": {
                        "summary": "Успешная авторизация",
                        "value": {
                            "status": "success",
                            "message": "Logged in"
                        }
                    },
                    "registered_and_logged_in": {
                        "summary": "Успешная регистрация и авторизация",
                        "value": {
                            "status": "success",
                            "message": "Registered and logged in"
                        }
                    },
                }
            }
        }
    },
    400: {
        "description": "Ошибка авторизации",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_login_data": {
                        "summary": "Ошибка",
                        "value": {
                            "detail": "Ошибка авторизации: <тип ошибки>"
                        }
                    }
                }
            }
        }
    },
    409: {
        "description": "Ошибка уникальности данных",
        "content": {
            "application/json": {
                "examples": {
                    "duplicate_telegram_id": {
                        "summary": "Пользователь с таким telegram_id уже существует",
                        "value": {
                            "detail": "Пользователь с таким telegram_id уже существует"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "examples": {
                    "database_error": {
                        "summary": "Ошибка базы данных",
                        "value": {
                            "detail": "Внутренняя ошибка базы данных: <тип ошибки>"
                        }
                    },
                    "unexpected_error": {
                        "summary": "Ошибка авторизации",
                        "value": {
                            "detail": "Внутренняя ошибка при авторизации: <тип ошибки>"
                        }
                    }
                }
            }
        }
    },
}
# Для эндпоинта /sessions/role в src/api/sessions
sessions_role_responses = {
    200: {
        "description": "Роль пользователя успешно получена",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "Роль получена",
                        "value": {
                            "status": "success",
                            "message": "Роль пользователя: 'test_user' получена",
                            "role": "admin"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Пользователь отсутствует",
                        "value": {
                            "status": "failed",
                            "message": "Пользователь с именем: 'test_user' не существует"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "examples": {
                    "server_error": {
                        "summary": "Ошибка сервера",
                        "value": {
                            "detail": "Внутренняя ошибка сервера: <тип ошибки>"
                        }
                    }
                }
            }
        }
    }
}
