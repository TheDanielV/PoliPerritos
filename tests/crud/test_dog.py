# Handle duplicate id_chip values causing IntegrityError
from datetime import date

from app.crud.dog import (
    create_static_dog,
    read_all_static_dogs,
    read_static_dogs_by_id,
    update_static_dog,
    delete_an_static_dog_by_id,
    create_adoption_dog,
    read_all_adoption_dogs,
    read_adoption_dog_by_id,
    update_adoption_dog,
    delete_an_adoption_dog_by_id,
    create_adopted_dog_without_commit,
    read_all_adopted_dogs,
    read_adopted_dogs_by_id,
    update_adopted_dog,
    unadopt_dog, adopt_dog,
)
from app.db.session import get_db
from app.models.domain.dog import Gender, StaticDog, AdoptionDog, AdoptedDog
from app.models.domain.owner import Owner
from app.models.schema.dog import StaticDogCreate, AdoptionDogCreate
from app.models.schema.owner import OwnerCreate
from main import app

from tests.conftest import setup_db, teardown_db, create_adoption_dog_for_tests, override_get_db, \
    create_auth_user_for_test

app.dependency_overrides[get_db] = override_get_db


# Test para perros estáticos

def test_create_static_dog():
    db = next(override_get_db())
    setup_db()

    test_dog = StaticDogCreate(
        id_chip=12345,
        name="Test Dog",
        about="A friendly dog",
        age=5,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    result = create_static_dog(db, test_dog)
    assert result == {"detail": "Perro Permanente creado"}
    teardown_db()


def test_read_all_static_dogs():
    db = next(override_get_db())
    setup_db()

    test_dog_1 = StaticDogCreate(
        id_chip=11111,
        name="Dog 1",
        about="First Dog",
        age=4,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    test_dog_2 = StaticDogCreate(
        id_chip=22222,
        name="Dog 2",
        about="Second Dog",
        age=2,
        is_vaccinated=False,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=True,
        operation="Operation",
    )
    create_static_dog(db, test_dog_1)
    create_static_dog(db, test_dog_2)

    result = read_all_static_dogs(db)
    assert len(result) == 2
    teardown_db()


def test_read_static_dogs_by_id():
    db = next(override_get_db())
    setup_db()

    test_dog = StaticDogCreate(
        id_chip=33333,
        name="Dog by ID",
        about="Specific Dog",
        age=1,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=True,
        operation="None",
    )
    create_static_dog(db, test_dog)
    dog = db.query(StaticDog).filter_by(id_chip=33333).first()

    result = read_static_dogs_by_id(db, dog.id)
    assert result.name == "Dog by ID"
    teardown_db()


def test_update_static_dog():
    db = next(override_get_db())
    setup_db()

    test_dog = StaticDogCreate(
        id_chip=44444,
        name="Dog to Update",
        about="Updatable Dog",
        age=6,
        is_vaccinated=False,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=False,
        operation="None",
    )
    create_static_dog(db, test_dog)
    dog = db.query(StaticDog).filter_by(id_chip=44444).first()

    updated_dog = StaticDogCreate(
        id_chip=44444,
        name="Updated Dog",
        about="Updated Description",
        age=7,
        is_vaccinated=True,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="Updated",
    )
    result = update_static_dog(db, updated_dog, dog.id)
    assert result == {"detail": "Perro Permanente Actualizado"}
    teardown_db()


def test_delete_an_static_dog_by_id():
    db = next(override_get_db())
    setup_db()

    test_dog = StaticDogCreate(
        id_chip=55555,
        name="Dog to Delete",
        about="Deletable Dog",
        age=3,
        is_vaccinated=False,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    create_static_dog(db, test_dog)
    dog = db.query(StaticDog).filter_by(id_chip=55555).first()

    result = delete_an_static_dog_by_id(db, dog.id)
    assert result is True
    teardown_db()


# Test para perros de adopción

def test_create_adoption_dog():
    db = next(override_get_db())
    setup_db()

    test_dog = AdoptionDogCreate(
        id_chip=10101,
        name="Adoption Dog 1",
        about="Friendly adoption dog",
        age=4,
        is_vaccinated=True,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    result = create_adoption_dog(db, test_dog)
    assert result == {"detail": "Perro de adopción creado"}
    teardown_db()


def test_read_all_adoption_dogs():
    db = next(override_get_db())
    setup_db()

    test_dog_1 = AdoptionDogCreate(
        id_chip=30303,
        name="Adoption Dog 4",
        about="First adoption dog",
        age=2,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    test_dog_2 = AdoptionDogCreate(
        id_chip=40404,
        name="Adoption Dog 5",
        about="Second adoption dog",
        age=6,
        is_vaccinated=False,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=False,
        operation="None",
    )
    create_adoption_dog(db, test_dog_1)
    create_adoption_dog(db, test_dog_2)

    result = read_all_adoption_dogs(db)
    assert len(result) == 2
    teardown_db()


def test_read_adoption_dog_by_id():
    db = next(override_get_db())
    setup_db()

    test_dog = AdoptionDogCreate(
        id_chip=50505,
        name="Adoption Dog by ID",
        about="Specific adoption dog",
        age=3,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=True,
        operation="None",
    )
    create_adoption_dog(db, test_dog)
    dog = db.query(AdoptionDog).filter_by(id_chip=50505).first()

    result = read_adoption_dog_by_id(db, dog.id)
    assert result.name == "Adoption Dog by ID"
    teardown_db()


def test_update_adoption_dog():
    db = next(override_get_db())
    setup_db()

    test_dog = AdoptionDogCreate(
        id_chip=60606,
        name="Adoption Dog to Update",
        about="Updatable adoption dog",
        age=5,
        is_vaccinated=False,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=False,
        operation="None",
    )
    create_adoption_dog(db, test_dog)
    dog = db.query(AdoptionDog).filter_by(id_chip=60606).first()

    updated_dog = AdoptionDogCreate(
        id_chip=60606,
        name="Updated Adoption Dog",
        about="Updated adoption dog description",
        age=6,
        is_vaccinated=True,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="Updated",
    )
    result = update_adoption_dog(db, updated_dog, dog.id)
    assert result == {"detail": "Perro de Adopción Actualizado"}
    teardown_db()


def test_delete_an_adoption_dog_by_id():
    db = next(override_get_db())
    setup_db()

    test_dog = AdoptionDogCreate(
        id_chip=70707,
        name="Adoption Dog to Delete",
        about="Deletable adoption dog",
        age=4,
        is_vaccinated=False,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    create_adoption_dog(db, test_dog)
    dog = db.query(AdoptionDog).filter_by(id_chip=70707).first()

    result = delete_an_adoption_dog_by_id(db, dog.id)
    assert result is True
    teardown_db()


# Test para perros adoptados

def test_adopt_dog():
    db = next(override_get_db())
    setup_db()

    # Crear un perro de adopción
    adoption_dog = AdoptionDog(
        id=1,
        id_chip=171717,
        name="Adopt Me",
        about="Adoption dog ready to find a home",
        age=3,
        is_vaccinated=True,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
    )
    db.add(adoption_dog)
    db.commit()

    # Crear un dueño
    owner_data = Owner(
        name="John Doe",
        direction="123 Adoption St.",
        cellphone="555-1234",
    )
    db.add(owner_data)
    db.commit()

    # Adoptar el perro
    adopted_dog = AdoptedDog(
        id=adoption_dog.id,
        id_chip=adoption_dog.id_chip,
        name=adoption_dog.name,
        about=adoption_dog.about,
        age=adoption_dog.age,
        is_vaccinated=adoption_dog.is_vaccinated,
        gender=adoption_dog.gender,
        image=adoption_dog.image,
        entry_date=adoption_dog.entry_date,
        is_sterilized=adoption_dog.is_sterilized,
        is_dewormed=adoption_dog.is_dewormed,
        operation=adoption_dog.operation,
        adopted_date=date.today(),
        owner=owner_data,
    )
    result = adopt_dog(db, adopted_dog)
    assert result == {"detail": "Perro Adoptado creado"}

    # Verificar que el perro fue adoptado
    adopted_dogs = read_all_adopted_dogs(db)
    assert len(adopted_dogs) == 1
    assert adopted_dogs[0].name == "Adopt Me"
    teardown_db()


def test_create_adopted_dog_without_commit():
    db = next(override_get_db())
    setup_db()

    # Crear un perro de adopción
    adoption_dog = AdoptionDog(
        id=2,
        id_chip=181818,
        name="Adopt Without Commit",
        about="Temporary adoption",
        age=2,
        is_vaccinated=False,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=False,
        operation="None",
    )
    db.add(adoption_dog)
    db.commit()

    # Crear un dueño
    owner = Owner(
        name="Jane Doe",
        direction="456 Temporary Ln.",
        cellphone="555-5678",
    )
    adopted_dog = AdoptedDog(
        id=adoption_dog.id,
        id_chip=adoption_dog.id_chip,
        name=adoption_dog.name,
        about=adoption_dog.about,
        age=adoption_dog.age,
        is_vaccinated=adoption_dog.is_vaccinated,
        gender=adoption_dog.gender,
        image=adoption_dog.image,
        entry_date=adoption_dog.entry_date,
        is_sterilized=adoption_dog.is_sterilized,
        is_dewormed=adoption_dog.is_dewormed,
        operation=adoption_dog.operation,
        adopted_date=date.today(),
        owner=owner,
    )

    # Crear sin hacer commit
    result = create_adopted_dog_without_commit(db, adopted_dog)
    assert result is not None
    assert result.name == "Adopt Without Commit"
    teardown_db()


def test_read_adopted_dogs_by_id():
    db = next(override_get_db())
    setup_db()

    # Crear perro adoptado
    adopted_dog = AdoptedDog(
        id=3,
        id_chip=191919,
        name="Adopted Dog By ID",
        about="Adopted dog details",
        age=5,
        is_vaccinated=True,
        image=None,
        gender=Gender.FEMALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=True,
        operation="None",
        adopted_date=date.today(),
        owner=Owner(
            name="Owner for Details",
            direction="789 Details Blvd.",
            cellphone="555-7890",
        ),
    )
    db.add(adopted_dog)
    db.commit()

    # Leer el perro por ID
    result = read_adopted_dogs_by_id(db, adopted_dog.id)
    assert result is not None
    assert result.name == "Adopted Dog By ID"
    teardown_db()


def test_update_adopted_dog():
    db = next(override_get_db())
    setup_db()

    # Crear perro adoptado
    adopted_dog = AdoptedDog(
        id=4,
        id_chip=202020,
        name="Update This Dog",
        about="Details to be updated",
        age=6,
        is_vaccinated=True,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=True,
        is_dewormed=False,
        operation="None",
        adopted_date=date.today(),
        owner=Owner(
            name="Initial Owner",
            direction="123 Initial St.",
            cellphone="555-1010",
        ),
    )
    db.add(adopted_dog)
    db.commit()

    # Actualizar el perro
    updated_data = AdoptionDogCreate(
        id_chip=202020,
        name="Updated Dog",
        about="Updated details",
        age=7,
        is_vaccinated=False,
        image=None,
        gender=Gender.MALE,
        entry_date=date.today(),
        is_sterilized=False,
        is_dewormed=True,
        operation="Updated Operation",
    )
    result = update_adopted_dog(db, updated_data, adopted_dog.id, image=None)
    assert result == {"detail": "Perro Adoptado Actualizado"}
    teardown_db()
