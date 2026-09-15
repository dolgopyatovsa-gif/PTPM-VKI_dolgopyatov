import hashlib
import logging
import sys
import os
import re


# Создаем папку для логов
os.makedirs("logs", exist_ok=True)


# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            "logs/file_txt.log",
            encoding="utf-8"
        )
    ]
)


# Запрещенные логины
BLACKLIST = {"admin", "administrator", "root", "user", "test"}


def hash_password(password):
    """Создает хеш пароля для записи в лог."""
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def is_valid_email(login):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.fullmatch(pattern, login):
        return True

    return False


def is_valid_phone(login):
    pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"

    if re.fullmatch(pattern, login):
        return True

    return False


def is_valid_username(login):
    if len(login) < 5:
        return False

    pattern = r"^[A-Za-z0-9_]+$"

    if re.fullmatch(pattern, login):
        return True

    return False


def check_password(password):
    """
    Проверяет пароль и возвращает конкретную причину ошибки.
    """

    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    # Проверяем наличие латинских букв
    if re.search(r"[A-Za-z]", password):
        return False, "Пароль не должен содержать латинские буквы"

    # Проверяем заглавную русскую букву
    if not re.search(r"[А-ЯЁ]", password):
        return False, "В пароле должна быть заглавная русская буква"

    # Проверяем строчную русскую букву
    if not re.search(r"[а-яё]", password):
        return False, "В пароле должна быть строчная русская буква"

    # Проверяем цифру
    if not re.search(r"\d", password):
        return False, "В пароле должна быть цифра"

    # Проверяем спецсимвол
    if not re.search(r"[^А-Яа-яЁё0-9]", password):
        return False, "В пароле должен быть специальный символ"

    return True, ""


def register_user(login, password, confirm_password):

    # Проверяем пустой логин
    if login == "":
        return False, "Логин не может быть пустым"

    # Проверяем черный список
    if login.lower() in BLACKLIST:
        return False, "Такой логин запрещен"

    # Проверяем email
    if is_valid_email(login):
        logging.debug("Логин распознан как email")

    # Проверяем телефон
    elif is_valid_phone(login):
        logging.debug("Логин распознан как телефон")

    # Проверяем обычный логин
    elif is_valid_username(login):
        logging.debug("Логин распознан как обычное имя пользователя")

    # Если ничего не подошло
    else:
        return False, (
            "Некорректный логин. "
            "Используйте email, телефон +x-xxx-xxx-xxxx "
            "или логин от 5 символов (латиница, цифры, _)"
        )

    # Проверяем пароль
    password_valid, password_message = check_password(password)

    if not password_valid:
        return False, password_message

    # Проверяем совпадение паролей
    if password != confirm_password:
        return False, "Пароль и подтверждение пароля не совпадают"

    return True, ""


def main():
    logging.info("Приложение запущено")

    try:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        confirm_password = input("Повторите пароль: ")

        # Пароль в лог не записываем.
        # Записываем только его хеш.
        logging.debug(
            "Получен запрос регистрации: login=%s, password_hash=%s",
            login,
            hash_password(password)
        )

        success, message = register_user(
            login,
            password,
            confirm_password
        )

        if success:
            logging.info(
                "Регистрация прошла успешно: login=%s, result=True",
                login
            )

            print("\nРегистрация прошла успешно!")


        else:
            logging.warning(
                "Регистрация не прошла: login=%s, result=False, причина=%s",
                login,
                message
            )

            print("\nРегистрация не прошла!")
            print("Причина:", message)

    except Exception:
        logging.exception("Произошла ошибка программы")

        print("\nПроизошла ошибка программы")


if __name__ == "__main__":
    main()
