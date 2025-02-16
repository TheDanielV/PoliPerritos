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

from tests.conftest import setup_db, teardown_db, create_adopted_dog_for_test, override_get_db, \
    create_auth_user_for_test, create_visit_for_test

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_new_visit():
    setup_db()
    create_auth_user_for_test()
    adopted = create_adopted_dog_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.post(f"/visits/create/",
                           headers={"Authorization": f"Bearer {token}"},
                           json={
                               "visit_date": "2025-02-16",
                               "evidence": None,
                               "observations": "None",
                               "adopted_dog_id": adopted
                           }
                           )
    assert response.status_code == 200
    assert "Visita Registrada" == response.json().get("detail")
    teardown_db()


def test_get_visits():
    setup_db()
    create_auth_user_for_test()
    visit = create_visit_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.get(f"/visits/all/",
                          headers={"Authorization": f"Bearer {token}"},
                          )
    assert response.status_code == 200
    assert visit == response.json()[0].get("id")
    teardown_db()


def test_get_visits_by_dog_id():
    setup_db()
    create_auth_user_for_test()
    visit = create_visit_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.get(f"/visits/all/20",
                          headers={"Authorization": f"Bearer {token}"},
                          )
    assert response.status_code == 200
    assert visit == response.json()[0].get("id")
    teardown_db()


def test_get_visits_by_id():
    setup_db()
    create_auth_user_for_test()
    visit = create_visit_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.get(f"/visits/{visit}",
                          headers={"Authorization": f"Bearer {token}"},
                          )
    assert response.status_code == 200
    assert visit == response.json().get("id")
    teardown_db()


def test_update_visit():
    setup_db()
    create_auth_user_for_test()
    visit = create_visit_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.put(f"/visits/update/",
                          headers={"Authorization": f"Bearer {token}"},
                          json={
                              "visit_date": "2025-02-16",
                              "evidence": None,
                              "observations": "Nuevo",
                              "adopted_dog_id": 20,
                              "id": visit
                          }
                          )
    assert response.status_code == 200

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response_get = client.get(f"/visits/{visit}",
                              headers={"Authorization": f"Bearer {token}"},
                              )
    assert response_get.json().get("observations") == "Nuevo"
    teardown_db()


def test_delete_visit_by_id():
    setup_db()
    create_auth_user_for_test()
    visit = create_visit_for_test()

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "SecurePassword123"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = client.delete(f"/visits/delete/{visit}",
                          headers={"Authorization": f"Bearer {token}"},
                          )
    assert response.status_code == 200
    assert "Visita eliminada" == response.json().get("message")
    teardown_db()