import re


def verify_password_(password: str):
    if len(password) < 8:
        return False
    patron = r'(?=.*[A-Z])(?=.*\d)'
    return bool(re.search(patron, password))


def verify_email(email: str):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.search(patron, email))


def verify_cellphone_number():
    pass
