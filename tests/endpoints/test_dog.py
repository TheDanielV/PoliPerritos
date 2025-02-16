from tkinter.font import names
from unittest import mock

from fastapi.testclient import TestClient
import pytest

from app.crud.user import create_auth_user
from app.db.session import get_db
from app.models.domain.dog import AdoptionDog, AdoptedDog
from app.models.domain.owner import Owner
from app.models.domain.user import Role
from app.models.schema.user import UserCreate
from main import app

from tests.conftest import setup_db, teardown_db, create_adoption_dog_for_tests, override_get_db, \
    create_auth_user_for_test

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_static_dog():
    setup_db()
    create_auth_user_for_test()
    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    # Se verifica que el perro disponible para adopción exista
    response = client.post("/dog/static_dog/create/",
                           headers={"Authorization": f"Bearer {token}"},
                           json={
                               "id_chip": 10,
                               "name": "string",
                               "about": "string",
                               "age": 10,
                               "is_vaccinated": False,
                               "image": None,
                               "gender": "male",
                               "entry_date": "2025-01-22",
                               "is_sterilized": False,
                               "is_dewormed": False,
                               "operation": "string"
                           })
    assert response.status_code == 200
    teardown_db()


def test_adopt_dog_by_id():
    setup_db()
    create_auth_user_for_test()
    adoption_dog = create_adoption_dog_for_tests()

    adoption_dog_db = next(override_get_db()).query(AdoptionDog).filter(AdoptionDog.id == adoption_dog).first()
    assert adoption_dog_db is not None
    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.post(f"/dog/adoption_dog/adopt/{adoption_dog}/2025-01-01",
                           headers={"Authorization": f"Bearer {token}"},
                           json={
                               "name": "Luis",
                               "direction": "Quitumbe",
                               "cellphone": "0979040404"
                           })
    assert response.status_code == 200
    assert "Perro Adoptado." == response.json().get("detail")
    adoption_dog_db = next(override_get_db()).query(AdoptionDog).filter(AdoptionDog.id == adoption_dog).first()
    assert adoption_dog_db is None
    adopted_dog_db = next(override_get_db()).query(AdoptedDog).filter(AdoptedDog.id == adoption_dog).first()
    assert adopted_dog_db is not None
    adopted_dog_db.owner.decrypt_owner_data()
    assert adopted_dog_db.owner.name == "Luis"
    teardown_db()


def test_adopt_dog_by_id_and_existing_owner():
    setup_db()
    create_auth_user_for_test()
    adoption_dog = create_adoption_dog_for_tests()
    db = next(override_get_db())
    existing_owner = Owner(id=1, name="Luis", direction="San Bartolo", cellphone="0998899876")
    existing_owner.crypt_owner_data()
    db.add(existing_owner)
    db.commit()
    adoption_dog_db = next(override_get_db()).query(AdoptionDog).filter(AdoptionDog.id == adoption_dog).first()
    assert adoption_dog_db is not None
    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.post(f"/dog/adoption_dog/adopt/{adoption_dog}/{existing_owner.id}/2025-01-01",
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "Perro Adoptado creado" == response.json().get("detail")
    adoption_dog_db = next(override_get_db()).query(AdoptionDog).filter(AdoptionDog.id == adoption_dog).first()
    assert adoption_dog_db is None
    adopted_dog_db = next(override_get_db()).query(AdoptedDog).filter(AdoptedDog.id == adoption_dog).first()
    assert adopted_dog_db is not None
    assert adopted_dog_db.owner.id == existing_owner.id
    teardown_db()
