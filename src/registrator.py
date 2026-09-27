import re

BLACKLIST = {"admin", "administrator", "root", "user", "test"}

def is_valid_email(login):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.fullmatch(pattern, login):
        return True
    else:
        return False

def is_valid_phone(phone):
    pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"

    if re.fullmatch(pattern, phone):
        return True
    else:
        return False

def is_valid_username(login):
    if len(login) < 5:
        return False

    pattern = r"^[A-Za-z0-9_]+$"

    if re.fullmatch(pattern, login):
        return True
    else:
        return False

def is_valid_password(password):
    if len(password) < 7:
        return False

    if re.search(r"[A-Za-z]", password):
        return False

    if not re.search(r"[А-ЯЁ]", password):
        return False

    if not re.search(r"[а-яё]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[^А-ЯЁа-яё0-9]", password):
        return False

    return True

def register_user(login, password, confirm_password):
    if login == "":
        return False, "Логин не может быть пустым"

    if login.lower() in BLACKLIST:
        return False, "Логин запрещен"

    valid_login = (
        is_valid_email(login)
        or is_valid_phone(login)
        or is_valid_username(login)
    )

    if not valid_login:
        return False, "Некорректный формат логина"

    if not is_valid_password(password):
        return False, "Пароль не соответствует требованиям"

    if password != confirm_password:
        return False, "Пароли не совпадают"

    return True, ""