from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.dog import AdoptedDog
from app.models.domain.visit import Visit
from app.models.schema.visit import VisitCreate, VisitUpdate


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
        db.refresh(adopted_dog.owner)
        db.add(db_visit)
        db.commit()
        db.refresh(db_visit)
        return {"detail": "Visita Registrada"}
    except IntegrityError:
        db.rollback()
        return None


def get_all_visits(db: Session):
    """
     Devuelve una lista de perros estáticos existentes.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.

     Returns:

     Example:
     ```
     ```
     """
    visits_raw = db.query(Visit).all()
    for visit in visits_raw:
        visit.adopted_dog.owner.decrypt_data()
    return visits_raw


def get_all_visits_by_dog(db: Session, dog_id: int):
    """
     Devuelve una lista de perros estáticos existentes.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.

     Returns:

     Example:
     ```
     ```
     """
    visits_raw = db.query(Visit).filter(Visit.adopted_dog_id == dog_id).all()
    for visit in visits_raw:
        visit.adopted_dog.owner.decrypt_data()
    return visits_raw


def read_visit_by_id(db: Session, visit_id: int):
    """
    Devuelve una visita por el id.
    """
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if visit:
        visit.adopted_dog.owner.decrypt_data()
    return visit


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
    except IntegrityError:
        db.rollback()
        return None


def delete_visit_by_id(db: Session, visit_id: int):
    """
    Deletes a user by their ID.

    Args:
        db (Session): Database session.
        visit_id (int): ID of the visit to delete.

    Raises:
        HTTPException: Raised with appropriate status codes and messages.
    """
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if visit is None:
        raise HTTPException(
            status_code=404, detail="Visita no encontrada."
        )
    else:
        try:
            db.delete(visit)
            db.commit()
            return {"success": True, "message": "Visita eliminada"}
        except IntegrityError as ie:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=ie
            )
