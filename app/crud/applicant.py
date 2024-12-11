from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.applicant import Applicant
from app.models.domain.course import Course
from app.models.schema.applicant import ApplicantCreate


def create_applicant(db: Session, applicant: ApplicantCreate, course: Course, image: bytes):
    db_applicant = Applicant(
        first_name=applicant.first_name,
        last_name=applicant.last_name,
        email=applicant.email,
        cellphone=applicant.cellphone,
        image=image,
        course_id=applicant.course_id
    )
    db_applicant.crypt_data()

    try:
        db.add(db_applicant)
        db.commit()
        return {"detail": "Solicitud registrada"}
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Error al actualizar el usuario. Por favor, inténtelo nuevamente."
        )


def read_all_applicants_by_course(db: Session, course_id):
    """Devuelve todos los usuarios.
    """
    applicants = db.query(Applicant).filter(Applicant.course_id == course_id).all()
    for applicant in applicants:
        applicant.decrypt_data()
    return applicants


def read_all_applicants_by_course_crypted(db: Session, course_id):
    """Devuelve todos los usuarios.
    """
    applicants = db.query(Applicant).filter(Applicant.course_id == course_id).all()
    return applicants


def read_applicant_by_id(db: Session, applicant_id):
    """Devuelve todos los usuarios.
    """
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if applicant:
        applicant.decrypt_data()
    return applicant


def read_number_of_applicants_by_course(db, course_id):
    applicants = read_all_applicants_by_course_crypted(db, course_id)
    count = len(applicants)
    if applicants:
        capacity = applicants[0].course.capacity
    else:
        capacity = 1
    return count, capacity


def delete_applicant_by_id(db: Session, applicant_id: int):
    """
    Deletes a applicant by their ID.

    Args:
        db (Session): Database session.
        applicant_id (int): ID of the visit to delete.

    Raises:
        HTTPException: Raised with appropriate status codes and messages.
    """
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()

    if Applicant is None:
        raise HTTPException(
            status_code=404, detail="Solicitud no encontrada."
        )
    else:
        try:
            db.delete(applicant)
            db.commit()
            return {"success": True, "message": "Solicitud eliminada"}
        except IntegrityError as ie:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=ie
            )
