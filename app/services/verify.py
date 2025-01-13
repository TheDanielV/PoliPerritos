import re


def verify_structure_password(password: str) -> bool:
    if len(password) < 8:
        return False
    patron = r'(?=.*[A-Z])(?=.*\d)'
    return bool(re.search(patron, password))


def verify_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.search(patron, email))


def verify_cellphone_number(cellphone: str) -> bool:
    if 10 >= len(cellphone) >= 7:
        patron = r'^\d+$'
        return bool(re.search(patron, cellphone))
    else:
        return False


def verify_hour(hour: str) -> bool:
    patron = r'^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$'
    return bool(re.search(patron, hour))
