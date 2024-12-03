from typing import List

from dns.dnssec import validate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import course
from app.crud.course import create_course, read_all_course, read_course_by_id, update_course_by_id, delete_course
from app.crud.owner import create_owner
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.course import CourseCreate, CourseResponse, CourseUpdate
from app.models.schema.owner import OwnerCreate
from app.models.schema.user import TokenData
from app.services.verify import verify_hour

router = APIRouter()


@router.post('/create', response_model=dict)
def create_new_course(course: CourseCreate,
                      db: Session = Depends(get_db),
                      current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for schedule in course.schedule:
        if not verify_hour(schedule.start_hour) and not verify_hour(schedule.end_hour):
            raise HTTPException(status_code=400, detail="Hora inválida")
    response = create_course(db, course)
    return response


@router.get('/', response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    response = read_all_course(db)
    if not response:
        raise HTTPException(status_code=404, detail="No se encontraron cursos")
    return response


@router.get('/{id_course}', response_model=CourseResponse)
def get_course_by_id(id_course: int,
                     db: Session = Depends(get_db)):
    response = read_course_by_id(db, id_course)
    if not response:
        raise HTTPException(status_code=404, detail="No se encontraron cursos")
    return response


@router.put('/update/{id_course}', response_model=dict)
def update_course(id_course: int,
                  course: CourseUpdate,
                  db: Session = Depends(get_db),
                  current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for schedule in course.schedule:
        if not verify_hour(schedule.start_hour) and not verify_hour(schedule.end_hour):
            raise HTTPException(status_code=400, detail="Hora inválida")
    response = update_course_by_id(db, course, id_course)
    return response


@router.delete('/delete/{course_id}', response_model=dict)
def delete_course_by_id(id_course: int,
                        db: Session = Depends(get_db),
                        current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    response = delete_course(db, id_course)
    return response
