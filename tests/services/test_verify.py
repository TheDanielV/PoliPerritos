from app.services.verify import verify_structure_password, verify_email, verify_cellphone_number, verify_hour


def test_valid_structure_password():
    valid_password = "SecurePassword123"
    assert verify_structure_password(valid_password)


def test_incorrect_structure_password():
    invalid_password = "1234"
    assert not verify_structure_password(invalid_password)


def test_invalid_email():
    invalid_email = "email"
    assert not verify_email(invalid_email)


def test_valid_email():
    invalid_email = "correct.email@email.com.ec"
    assert verify_email(invalid_email)


def test_invalid_cellphone_number_whit_letters():
    invalid_cellphone = "09e8877654"
    assert not verify_cellphone_number(invalid_cellphone)


def test_invalid_longest_cellphone_number():
    invalid_cellphone = "0998877651234"
    assert not verify_cellphone_number(invalid_cellphone)


def test_invalid_shortest_cellphone_number():
    invalid_cellphone = "2626"
    assert not verify_cellphone_number(invalid_cellphone)


def test_verify_cellphone_number():
    valid_cellphone = "0979047494"
    assert verify_cellphone_number(valid_cellphone)


def test_invalid_hour():
    invalid_hour = "22"
    assert not verify_hour(invalid_hour)


def test_valid_hour():
    valid_hour = "22:03"
    assert verify_hour(valid_hour)
