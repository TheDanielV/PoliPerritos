from app.models.domain.user import Role, User
import random
import string
import hashlib

from app.services.crypt import get_password_hash


def user_generator(email: str, role: Role) -> tuple[User, dict]:
    email_hash = hashlib.md5(email.encode()).hexdigest()[:6]  # Tomar 6 caracteres del hash
    username = f"{role.value}{email_hash}"
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=12))
    new_user = User(
        username=username,
        hashed_password=get_password_hash(password),
        email=email,
        role=role,
        is_active=False
    )
    data_for_email = {"body": {"username": username, "password": password}}
    return new_user, data_for_email

