from app.services.crypt import verify_password, get_password_hash


def test_hash_a_password():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
