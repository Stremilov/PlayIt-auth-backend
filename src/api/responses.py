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
# Для эндпоинта /users/whoami в src.api.whoami
whoami_responses = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "user_found": {
                        "summary": "Пользователь найден",
                        "value": {
                            "status": "success",
                            "message": "Пользователь по этому jwt-токену найден.",
                            "user": {
                                "id": 1,
                                "username": "example_user",
                                "telegram_id": 123456789,
                                "balance": 100,
                                "role": "USER",
                                "done_tasks": 10,
                                "group_number": "1A"
                            }
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Пользователь не авторизован",
        "content": {
            "application/json": {
                "examples": {
                    "not_authorized": {
                        "summary": "JWT-токен отсутствует или невалиден",
                        "value": {
                            "detail": "Не авторизован"
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
                    "user_not_found": {
                        "summary": "Пользователь не найден в базе данных",
                        "value": {
                            "detail": "Пользователь не найден"
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
                    "unexpected_error": {
                        "summary": "Неожиданная ошибка",
                        "value": {
                            "detail": "Произошла непредвиденная ошибка: <тип ошибки>"
                        }
                    }
                }
            }
        }
    }
}

update_user_balance_responses = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "successful operation": {
                        "summary": "Баланс изменен",
                        "value": {
                            "status": "success",
                            "message": "Баланс пользователя успешно обновлен",
                            "user": {
                                "id": 1,
                                "username": "example_user",
                                "telegram_id": 123456789,
                                "balance": 100,
                                "role": "USER",
                                "done_tasks": 10,
                                "group_number": "1A"
                            }
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Пользователь не авторизован",
        "content": {
            "application/json": {
                "examples": {
                    "not_authorized": {
                        "summary": "JWT-токен отсутствует или невалиден",
                        "value": {
                            "detail": "Не авторизован"
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
                    "user_not_found": {
                        "summary": "Пользователь не найден в базе данных",
                        "value": {
                            "detail": "Пользователь не найден"
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
                    "unexpected_error": {
                        "summary": "Неожиданная ошибка",
                        "value": {
                            "detail": "Произошла непредвиденная ошибка: <тип ошибки>"
                        }
                    }
                }
            }
        }
    }
}