import pytest
from httpx import AsyncClient

from main import app
from tests.conftest import init_test_db


@pytest.mark.asyncio
async def test_login_valid_credentials(setup_db):
    """
    Prueba de inicio de sesión con credenciales válidas.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/token",
            data={"username": "admin", "password": "SecurePassword123"}
        )
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """
    Prueba de inicio de sesión con credenciales inválidas.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/token",
            data={"username": "invalid_user", "password": "WrongPassword"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_protected_route_with_valid_token():
    """
    Prueba de acceso a una ruta protegida con un token válido.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Simulamos obtener un token válido
        token_response = await ac.post(
            "/auth/token",
            data={"username": "admin", "password": "SecurePassword123"}
        )
        token = token_response.json()["access_token"]

        # Intentamos acceder a una ruta protegida con el token
        response = await ac.get(
            "/auth/",  # Cambia esto por la ruta real protegida
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_protected_route_with_invalid_token():
    """
    Prueba de acceso a una ruta protegida con un token inválido.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/generate_user?email=email%40email.com&role=admin'",  # Cambia esto por la ruta real protegida
            headers={"Authorization": "Bearer INVALID_TOKEN"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
