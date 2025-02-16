from datetime import date

from app.crud.visit import create_a_visit, get_all_visits, get_all_visits_by_dog, read_visit_by_id, update_visit, \
    delete_visit_by_id
from app.db.session import get_db
from app.models.domain.dog import Gender, StaticDog, AdoptionDog, AdoptedDog
from app.models.domain.owner import Owner
from app.models.domain.visit import Visit
from app.models.schema.dog import StaticDogCreate, AdoptionDogCreate
from app.models.schema.owner import OwnerCreate
from app.models.schema.visit import VisitCreate, VisitUpdate
from main import app

from tests.conftest import setup_db, teardown_db, create_adoption_dog_for_tests, override_get_db, \
    create_auth_user_for_test, create_adopted_dog_for_test, create_visit_for_test

app.dependency_overrides[get_db] = override_get_db


def test_create_a_visit():
    """Prueba la creación de una visita."""
    db = next(override_get_db())
    setup_db()
    dog = create_adopted_dog_for_test()
    visit_data = VisitCreate(
        visit_date=date.today(),
        evidence=None,
        observations="El perro está sano",
        adopted_dog_id=dog,
    )
    result = create_a_visit(db, visit_data, db.query(AdoptedDog).filter(AdoptedDog.id == dog).first())
    assert result == {"detail": "Visita Registrada"}
    teardown_db()


def test_get_all_visits():
    """Prueba la obtención de todas las visitas registradas."""
    db = next(override_get_db())
    setup_db()
    create_visit_for_test()
    visits = get_all_visits(db)
    assert len(visits) > 0
    teardown_db()


def test_get_all_visits_by_dog():
    """Prueba la obtención de todas las visitas registradas."""
    db = next(override_get_db())
    setup_db()
    create_visit_for_test()
    visit = get_all_visits_by_dog(db, 20)
    assert len(visit) > 0
    teardown_db()


def test_read_visit_by_id():
    """Prueba la obtención de una visita registrada."""
    db = next(override_get_db())
    setup_db()
    visit_id = create_visit_for_test()
    visit = read_visit_by_id(db, visit_id)
    assert visit_id == visit.id
    teardown_db()


def test_update_visit():
    """Prueba actualizar una visita."""
    db = next(override_get_db())
    setup_db()
    visit_id = create_visit_for_test()
    dog = db.query(AdoptedDog).filter(AdoptedDog.id == 20).first()
    updated_data = VisitUpdate(
        id=visit_id,
        visit_date=date.today(),
        evidence=None,
        observations="Observaciones actualizadas",
        adopted_dog_id=dog.id,
    )

    result = update_visit(db, updated_data, dog)
    assert result == {"detail": "Visita Actualizada"}
    teardown_db()


def test_delete_visit_by_id():
    """Prueba eliminar una visita."""
    db = next(override_get_db())
    setup_db()
    visit_id = create_visit_for_test()

    result = delete_visit_by_id(db, visit_id)
    assert result == dict(success=True, message="Visita eliminada")
    teardown_db()
