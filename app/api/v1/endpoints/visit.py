import base64
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.dog import read_adopted_dogs_by_id
from app.crud.visit import create_a_visit, get_all_visits, get_all_visits_by_dog, read_visit_by_id, update_visit
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.schema.user import TokenData
from app.models.schema.visit import VisitCreate, VisitResponse, VisitUpdate

from app.models.domain.user import Role
from app.services.images_control_service import verify_image_size

router = APIRouter()


@router.post('/create/', response_model=dict)
async def create_new_visit(visit: VisitCreate,
                           db: Session = Depends(get_db),
                           current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Create a visit for an adopted dog:

    - **visit_date** (required): date of the visit in format YYYY-MM-DD.
    - **evidence** (required): base64 encrypted image of a evidence of the visit.
    - **observations** (optional): any observation of the visit.
    - **adopted_dog_id** (required): id of the dog visited.

    Español:
    --------
    Crear una visita para un perro adoptado:

    - **visit_date** (required): fecha de la visita en formato YYYY-MM-DD.
    - **evidence** (required): imagen encriptada en base 64 de la visita.
    - **observations** (optional): observación de la visita.
    - **adopted_dog_id** (required): id del perro visitado.
    """

    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image_data = None
    if visit.evidence:
        try:
            image_data = base64.b64decode(visit.evidence)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    # verificamos el tamaño de la imagen
    try:
        verify_image_size(image_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image size")

    # Obtenemos el perro
    adopted_dog = read_adopted_dogs_by_id(db, visit.adopted_dog_id)
    adopted_dog.owner.crypt_data()
    if not adopted_dog:
        raise HTTPException(status_code=404, detail=f'No se encontro al perro con id: {visit.adopted_dog_id}')
    result = create_a_visit(db, visit, adopted_dog, image_data)
    if result is None:
        raise HTTPException(status_code=409, detail="La visita que desea registrar ya existe")
    return result


@router.get('/all/', response_model=List[VisitResponse])
async def get_visits(db: Session = Depends(get_db),
                     current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get all visits.

    Español:
    --------
    Lee todas las visitas.

    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    visits_raw = get_all_visits(db)
    if not visits_raw:
        raise HTTPException(status_code=404, detail="No hay visitas")
    visits = []
    for visit in visits_raw:
        if isinstance(visit.adopted_dog.image, bytes):
            data = base64.b64encode(visit.adopted_dog.image).decode('utf-8') if visit.evidence else None
        else:
            data = visit.adopted_dog.image
        evidence_base64 = base64.b64encode(visit.evidence).decode('utf-8') if visit.evidence else None

        visit.adopted_dog.image = f'{data}'
        visit.evidence = evidence_base64

        visits.append(visit)

    return visits


@router.get('/all/{dog_id}', response_model=List[VisitResponse])
async def get_visits_by_dog_id(dog_id: int, db: Session = Depends(get_db),
                               current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get all visits by dog id.

    Español:
    --------
    Lee todas las visitas por el id del perro.

    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image_data = None
    visits_raw = get_all_visits_by_dog(db, dog_id)
    if not visits_raw:
        raise HTTPException(status_code=404, detail="No hay visitas")
    visits = []
    for visit in visits_raw:
        if isinstance(visit.adopted_dog.image, bytes):
            data = base64.b64encode(visit.adopted_dog.image).decode('utf-8') if visit.evidence else None
        else:
            data = visit.adopted_dog.image
        evidence_base64 = base64.b64encode(visit.evidence).decode('utf-8') if visit.evidence else None

        visit.adopted_dog.image = f'{data}'
        visit.evidence = evidence_base64

        visits.append(visit)

    return visits


@router.get('/{visit_id}', response_model=VisitResponse)
async def get_visit_by_id(visit_id: int, db: Session = Depends(get_db),
                          current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get a visits by id.

    Español:
    --------
    Lee una las visitas por el id.

    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    visit = read_visit_by_id(db, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="No hay visitas")

    image_base64 = base64.b64encode(visit.adopted_dog.image).decode('utf-8') if visit.adopted_dog.image else None

    evidence_base64 = base64.b64encode(visit.evidence).decode('utf-8') if visit.evidence else None

    visit.adopted_dog.image = image_base64
    visit.evidence = evidence_base64

    return visit


@router.put('/update/', response_model=dict)
async def update_visit_by_id(visit_update: VisitUpdate, db: Session = Depends(get_db),
                             current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update a visit for an adopted dog:

    - **visit_date** (required): date of the visit in format YYYY-MM-DD.
    - **evidence** (required): base64 encrypted image of a evidence of the visit.
    - **observations** (optional): any observation of the visit.
    - **adopted_dog_id** (required): id of the dog visited.
    - **id** (required): id of the visit to be updated.

    Español:
    --------
    Actualiza una visita para un perro adoptado:

    - **visit_date** (required): fecha de la visita en formato YYYY-MM-DD.
    - **evidence** (required): imagen encriptada en base 64 de la visita.
    - **observations** (optional): observación de la visita.
    - **adopted_dog_id** (required): id del perro visitado.
    - **id** (required): id de la visita a ser actualizada.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Verificamos la imagen
    image_data = None
    if visit_update.evidence:
        try:
            image_data = base64.b64decode(visit_update.evidence)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    else:
        image_data = read_visit_by_id(db, visit_update.id).evidence
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")

    # Verificamos que el perro asociado a la visita exista
    adopted_dog = read_adopted_dogs_by_id(db, visit_update.adopted_dog_id)
    adopted_dog.owner.crypt_data()
    if not adopted_dog:
        raise HTTPException(status_code=404, detail=f'No se encontro al perro con id: {visit_update.adopted_dog_id}')
    result = update_visit(db, visit_update, adopted_dog, image_data)
    if result is None:
        raise HTTPException(status_code=409, detail="Hubo un problema al actualizar")
    return result
