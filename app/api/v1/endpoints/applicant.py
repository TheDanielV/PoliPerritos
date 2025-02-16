import base64
import io
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.core.security import get_current_user
from app.crud.applicant import create_applicant, read_all_applicants_by_course, read_number_of_applicants_by_course, \
    read_applicant_by_id, delete_applicant_by_id
from app.crud.course import read_course_by_id
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.applicant import ApplicantCreate, ApplicantResponse
from app.models.schema.user import TokenData
from app.services.images_control_service import verify_image_size

router = APIRouter()

load_dotenv()

API_URL = os.getenv("API_URL")


@router.post('/create/', response_model=dict)
async def create_new_applicant(applicant: ApplicantCreate,
                               db: Session = Depends(get_db)):
    image_data = None
    if applicant.image:
        try:
            image_data = base64.b64decode(applicant.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    # verificamos el tamaño de la imagen
    try:
        verify_image_size(image_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image size")

    # Obtenemos el curso
    course = read_course_by_id(db, applicant.course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f'No se encontro al curso con id: {applicant.course_id}')
    count, capacity = read_number_of_applicants_by_course(db, applicant.course_id)
    if count < capacity:
        result = create_applicant(db, applicant, course, image_data)
        return result
    else:
        raise HTTPException(status_code=404, detail=f'No hay más cupos')


@router.get('/course/{course_id}/all/', response_model=List[ApplicantResponse])
async def get_applicants_by_course(course_id: int,
                                   db: Session = Depends(get_db),
                                   current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get all visits.

    Español:
    --------
    Lee todas las visitas.

    """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    applicant_raw = read_all_applicants_by_course(db, course_id)
    if not applicant_raw:
        raise HTTPException(status_code=404, detail="No hay solicitudes")
    for applicant in applicant_raw:
        if applicant.image:
            applicant.image = f'{API_URL}/applicant/{applicant.id}/image'
    return applicant_raw


@router.get('/{applicant_id}', response_model=ApplicantResponse)
async def get_applicant_by_id(applicant_id: int, db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get a applicant by id.

    Español:
    --------
    Lee una las solicitudes por el id.

    """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    applicant = read_applicant_by_id(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="No hay solicitantes")

    if applicant.image:
        applicant.image = f'{API_URL}/applicant/{applicant.id}/image'

    return applicant


@router.get("/{applicant_img}/image", response_class=StreamingResponse)
def get_applicant_img(applicant_img: int, db: Session = Depends(get_db),
                      current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    applicant = read_applicant_by_id(db, applicant_img)
    if not applicant or not applicant.image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return StreamingResponse(io.BytesIO(applicant.image), media_type="image/jpeg")


@router.delete('/delete/{id_visit}', response_model=dict)
def delete_an_applicant_by_id(id_applicant: int, db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Delete a visit:

    - **id_visit** (required): Id of the visit.

    Español:
    --------
    Borrar una visita:

    - **id_visit** (required): ID de la visita.
    """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    applicant_response = delete_applicant_by_id(db, id_applicant)
    return applicant_response
