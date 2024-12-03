from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.course import Course
from app.models.domain.schedule import Schedule
from app.models.domain.token import AuthToken
from app.models.schema.course import CourseCreate


def create_course(db: Session, course: CourseCreate) -> dict:
    """

    :rtype: dict
    """
    db_course = Course(
        name=course.name,
        description=course.description,
        start_date=course.start_date,
        end_date=course.end_date,
        price=course.price
    )
    for schedule in course.schedule:
        sch = Schedule(
            day=schedule.day,
            start_hour=schedule.start_hour,
            end_hour=schedule.end_hour
        )
        db_course.schedule.append(sch)

    try:
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return {"message": "Curso creado"}
    except IntegrityError as ie:
        db.rollback()
        error_message = str(ie.orig)
        if "Duplicate entry" in error_message:
            raise HTTPException(
                status_code=400, detail="El curso ya existe."
            )
        raise HTTPException(
            status_code=500, detail="Error al crear el curso. Por favor, inténtelo nuevamente."
        )


def read_all_course(db: Session) -> List[Course]:
    """

    :param db:
    :return: List[Course]
    """
    return db.query(Course).all()


def read_course_by_id(db: Session, course_id: int) -> Course:
    """

    :param db:
    :param course_id:
    :return:
    """
    return db.query(Course).filter(Course.id == course_id).first()


def update_course_by_id(db: Session, course: CourseCreate, course_id: int):
    db_course = Course(
        id=course_id,
        name=course.name,
        description=course.description,
        start_date=course.start_date,
        end_date=course.end_date,
        price=course.price
    )
    for schedule in course.schedule:
        sch = Schedule(
            day=schedule.day,
            start_hour=schedule.start_hour,
            end_hour=schedule.end_hour
        )
        db_course.schedule.append(sch)
    try:
        db.merge(db_course)
        db.commit()
        return {"detail": "Curso actualizado"}
    except IntegrityError as ie:
        db.rollback()
        print(ie)
        return HTTPException(status_code=403, detail="could not update")


def delete_course(db: Session, course_id: int):
    """
    Deletes a user by their ID.

    Args:
        db (Session): Database session.
        course_id (int): ID of the user to delete.

    Raises:
        HTTPException: Raised with appropriate status codes and messages.
    """
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=404, detail="Curso no encontrado."
        )
    else:
        try:
            db.delete(course)
            db.commit()
            return {"success": True, "message": "Curso eliminado"}
        except IntegrityError as ie:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=ie
            )
