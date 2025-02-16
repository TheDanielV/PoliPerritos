import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from app.crud.dog import create_adoption_dog
from app.crud.user import create_auth_user
from app.db.database import Base
from app.db.session import get_db
from app.models.domain.dog import AdoptionDog, Gender
from app.models.domain.user import Role
from app.models.schema.user import UserCreate

DATABASE_URL = "sqlite:///:memory:"

# Configuración de la base de datos de prueba
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función para crear las tablas
def setup_db() -> None:
    Base.metadata.create_all(bind=engine)


# Función para eliminar las tablas
def teardown_db() -> None:
    Base.metadata.drop_all(bind=engine)


# Dependency para reemplazar get_db durante las pruebas
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_adoption_dog_for_tests() -> int:
    db = next(override_get_db())
    db_adoption_dog = AdoptionDog(
        id=20,
        id_chip=2020,
        name="Firulais",
        about="Perro alegre",
        age=3,
        is_vaccinated=True,
        gender=Gender.MALE,
        image=None,
        entry_date=None,
        is_sterilized=True,
        is_dewormed=True,
        operation="Sin operaciones"
    )
    # Crear perro de adopción
    db.add(db_adoption_dog)
    db.commit()
    return db_adoption_dog.id


def create_auth_user_for_test():
    db = next(override_get_db())

    auth_user = UserCreate(username="admin",
                           email="admin@base.com",
                           password="SecurePassword123",
                           role=Role.ADMIN)
    create_auth_user(db, auth_user)
