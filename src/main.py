import hashlib
import logging
import sys
import os

from src.registrator import register_user

os.makedirs("logs", exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            "logs/file_txt.log",
            encoding="utf-8"
        )
    ]
)

def hash_password(password):

    password_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    return password_hash

def main():
    logging.info("Приложение запущено")

    try:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        confirm_password = input("Повторите пароль: ")

        logging.debug(
            "Получен запрос для регистрации: login=%s, password_hash=%s",
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
                "Регистрация прошла успешно: login=%s",
                login
            )

            print("\nРегистрация прошла успешно!")

        else:
            logging.warning(
                "Регистрация не прошла: login=%s, причина=%s",
                login,
                message
            )

            print("\nОшибка:", message)

    except Exception:
        logging.error(
            "Произошла ошибка"
        )

        print("\nПроизошла ошибка программы")

if __name__ == "__main__":
    main()