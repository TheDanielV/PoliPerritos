from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.dog import AdoptedDog
from app.models.domain.visit import Visit
from app.models.schema.visit import VisitCreate, VisitResponse, VisitUpdate


def create_a_visit(db: Session, visit: VisitCreate, adopted_dog: AdoptedDog, evidence: bytes = None):
    """

     """

    db_visit = Visit(
        visit_date=visit.visit_date,
        evidence=evidence,
        observations=visit.observations,
        adopted_dog=adopted_dog
    )
    try:
        db.add(db_visit)
        db.commit()
        db.refresh(db_visit)
        return {"detail": "Visita Registrada"}
    except IntegrityError as ie:
        db.rollback()
        return None


def get_all_visits(db: Session):
    """
     Devuelve una lista de perros estaticos existentes.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.

     Returns:

     Example:
     ```
     ```
     """
    return db.query(Visit).all()


def get_all_visits_by_dog(db: Session, dog_id: int):
    """
     Devuelve una lista de perros estaticos existentes.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.

     Returns:

     Example:
     ```
     ```
     """
    return db.query(Visit).filter(Visit.adopted_dog_id == dog_id).all()


def read_visit_by_id(db: Session, visit_id: int):
    """
    Devuelve una visita por el id.
    """
    return db.query(Visit).filter(Visit.id == visit_id).first()


def update_visit(db: Session, visit_update: VisitUpdate, adopted_dog: AdoptedDog, evidence: bytes = None):
    db_visit_update = Visit(
        id=visit_update.id,
        visit_date=visit_update.visit_date,
        evidence=evidence,
        observations=visit_update.observations,
        adopted_dog=adopted_dog
    )
    try:
        db.merge(db_visit_update)
        db.commit()
        return {"detail": "Visita Actualizada"}
    except IntegrityError as ie:
        db.rollback()
        return None
