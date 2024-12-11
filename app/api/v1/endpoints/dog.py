import base64
import io
import os
from datetime import date
from typing import List

import dotenv
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.dog import read_all_static_dogs, read_static_dogs_by_id, create_static_dog, delete_an_static_dog_by_id, \
    read_all_adoption_dogs, read_adoption_dog_by_id, create_adoption_dog, delete_an_adoption_dog_by_id, \
    read_all_adopted_dogs, read_adopted_dogs_by_id, update_static_dog, update_adoption_dog, update_adopted_dog, \
    adopt_dog
from app.crud.owner import read_owner_by_id
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.dog import StaticDogResponse, StaticDogCreate, AdoptionDogResponse, AdoptionDogCreate, \
    AdoptedDogResponse, AdoptedDogUpdate
from app.models.schema.owner import OwnerCreate, OwnerResponse
from app.models.schema.user import TokenData
from app.services.images_control_service import verify_image_size
from app.services.multi_crud_service import create_owner_and_adopted_dog, un_adopt_dog_service

router = APIRouter()

load_dotenv()

API_URL = os.getenv("API_URL")


@router.post('/static_dog/create/', response_model=dict)
async def create_new_static_dog(dog: StaticDogCreate,
                                db: Session = Depends(get_db),
                                current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Create a static dog:

    - **id_chip** (optional): chip of the dog.
    - **name** (required): Name of the dog.
    - **about** (optional): Description of the dog.
    - **age** (required): Age of the dog.
    - **is_vaccinated** (required): Indicates if the dog is vaccinated. Must be a boolean:
        - **true**: The dog is vaccinated.
        - **false**: The dog is not vaccinated.
    - **image** (optional): Base64 encrypted image of the dog.
    - **gender** (required): Gender of the dog. Must be one of:
        - **male**: Represents a male dog.
        - **female**: Represents a female dog.
    - **entry_date** (optional): Date of the entry in format YYYY-MM-DD.
    - **is_sterilized** (required): Indicates if the dog is sterilized. Must be a boolean:
        - **true**: The dog is sterilized.
        - **false**: The dog is not sterilized
    - **is_dewormed** (required): Indicates if the dog is dewormed. Must be a boolean:
        - **true**: The dog is dewormed.
        - **false**: The dog is not dewormed
    - **operation** (optional): Specify the operation of the dog.

    Español:
    --------
    Crear un perro estático:

    - **id_chip** (optional): Chip del perro.
    - **name** (required): Nombre del perro.
    - **about** (optional): Descripción del perro.
    - **age** (required): Edad del perro.
    - **is_vaccinated** (required): Indica si el perro esta vacunado. Debe ser un boolean:
        - **true**: El perro esta vacunado.
        - **false**: El perro no esta vacunado.
    - **image** (optional): Imagen del perro encriptad en base64.
    - **gender** (required): Genero del perro. Debe ser uno de los siguientes:
        - **male**: Representa un perro macho.
        - **female**: Representa un perro hembra.
    - **entry_date** (optional): Fecha de entrada en formato YYYY-MM-DD.
    - **is_sterilized** (required): Indica si el perro esta esterilizado. Debe ser un boolean:
        - **true**: El perro esta esterilizado.
        - **false**: El perro no esta esterilizado.
    - **is_dewormed** (required): Indica si el perro esta desparasitado. Debe ser un boolean:
        - **true**: El perro esta desparasitado.
        - **false**: El perro no esta desparasitado.
    - **operation** (optional): Especifica la/las operaciones del perro.
    """

    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image_data = None
    if dog.image:
        try:
            image_data = base64.b64decode(dog.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
        # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")

    # Crear el perro en la base de datos
    result = create_static_dog(db, dog, image_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result


@router.get('/static_dog/', response_model=List[StaticDogResponse])
def get_static_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros estáticos.
    """
    static_dogs = read_all_static_dogs(db)

    if not static_dogs:
        raise HTTPException(status_code=404, detail="No se encontraron perros estáticos")
    for dog in static_dogs:
        if dog.image:
            dog.image = f'{API_URL}/dog/static_dog/{dog.id}/image'
    return static_dogs


@router.get('/static_dog/{dog_id}', response_model=StaticDogResponse)
def get_static_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    static_dog = read_static_dogs_by_id(db, dog_id)

    if not static_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros estáticos")
    # noinspection PyTypeChecker
    if static_dog.image:
        static_dog.image = f'{API_URL}/dog/static_dog/{static_dog.id}/image'
    return static_dog


@router.get("/static_dog/{dog_id}/image", response_class=StreamingResponse)
def get_static_dog_image(dog_id: int, db: Session = Depends(get_db)):
    static_dog = read_static_dogs_by_id(db, dog_id)
    if not static_dog or not static_dog.image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return StreamingResponse(io.BytesIO(static_dog.image), media_type="image/jpeg")


@router.put('/static_dog/update/{id_dog}', response_model=dict)
async def update_a_static_dog(id_dog: int,
                              dog: StaticDogCreate,
                              db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update a static dog:

    - **id_chip** (optional): chip of the dog.
    - **name** (required): Name of the dog.
    - **about** (optional): Description of the dog.
    - **age** (required): Age of the dog.
    - **is_vaccinated** (required): Indicates if the dog is vaccinated. Must be a boolean:
        - **true**: The dog is vaccinated.
        - **false**: The dog is not vaccinated.
    - **image** (optional): Base64 encrypted image of the dog.
    - **gender** (required): Gender of the dog. Must be one of:
        - **male**: Represents a male dog.
        - **female**: Represents a female dog.
    - **entry_date** (optional): Date of the entry in format YYYY-MM-DD.
    - **is_sterilized** (required): Indicates if the dog is sterilized. Must be a boolean:
        - **true**: The dog is sterilized.
        - **false**: The dog is not sterilized
    - **is_dewormed** (required): Indicates if the dog is dewormed. Must be a boolean:
        - **true**: The dog is dewormed.
        - **false**: The dog is not dewormed
    - **operation** (optional): Specify the operation of the dog.

    Español:
    --------
    Actualizar un perro estático:

    - **id_chip** (optional): Chip del perro.
    - **name** (required): Nombre del perro.
    - **about** (optional): Descripción del perro.
    - **age** (required): Edad del perro.
    - **is_vaccinated** (required): Indica si el perro esta vacunado. Debe ser un boolean:
        - **true**: El perro esta vacunado.
        - **false**: El perro no esta vacunado.
    - **image** (optional): Imagen del perro encriptad en base64.
    - **gender** (required): Genero del perro. Debe ser uno de los siguientes:
        - **male**: Representa un perro macho.
        - **female**: Representa un perro hembra.
    - **entry_date** (optional): Fecha de entrada en formato YYYY-MM-DD.
    - **is_sterilized** (required): Indica si el perro esta esterilizado. Debe ser un boolean:
        - **true**: El perro esta esterilizado.
        - **false**: El perro no esta esterilizado.
    - **is_dewormed** (required): Indica si el perro esta desparasitado. Debe ser un boolean:
        - **true**: El perro esta desparasitado.
        - **false**: El perro no esta desparasitado.
    - **operation** (optional): Especifica la/las operaciones del perro.
    """
    # TODO validar en caso de que se actualice también el id
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if dog.image:
        try:
            image_data = base64.b64decode(dog.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    else:
        db_dog = read_static_dogs_by_id(db, id_dog)
        if db_dog:
            image_data = db_dog.image
        else:
            raise HTTPException(status_code=404, detail="Perro no encontrado")
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")
    # Crear el perro en la base de datos
    result = update_static_dog(db, dog, id_dog, image_data)
    if result is None:
        raise HTTPException(status_code=409, detail="Error al actualizar el perro")
    return result


@router.delete('/static_dog/delete/{id_static_dog}', response_model=dict)
def delete_static_dog_by_id(id_static_dog: int, db: Session = Depends(get_db),
                            current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para borrar un perro estatico.
    """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dog_response = delete_an_static_dog_by_id(db, id_static_dog)
    if dog_response:
        return {"success": True, "message": "Perro Permanente Borrado"}
    else:
        return {"success": False, "message": "Perro Permanente no eliminado"}


# 4 Adoption dog

@router.post('/adoption_dog/create/', response_model=dict)
def create_new_adoption_dog(dog: AdoptionDogCreate, db: Session = Depends(get_db),
                            current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Create an adoption dog:

    - **id_chip** (optional): chip of the dog.
    - **name** (required): Name of the dog.
    - **about** (optional): Description of the dog.
    - **age** (required): Age of the dog.
    - **is_vaccinated** (required): Indicates if the dog is vaccinated. Must be a boolean:
        - **true**: The dog is vaccinated.
        - **false**: The dog is not vaccinated.
    - **image** (optional): Base64 encrypted image of the dog.
    - **gender** (required): Gender of the dog. Must be one of:
        - **male**: Represents a male dog.
        - **female**: Represents a female dog.
    - **entry_date** (optional): Date of the entry in format YYYY-MM-DD.
    - **is_sterilized** (required): Indicates if the dog is sterilized. Must be a boolean:
        - **true**: The dog is sterilized.
        - **false**: The dog is not sterilized
    - **is_dewormed** (required): Indicates if the dog is dewormed. Must be a boolean:
        - **true**: The dog is dewormed.
        - **false**: The dog is not dewormed
    - **operation** (optional): Specify the operation of the dog.

    Español:
    --------
    Crear un perro de adopción:

    - **id_chip** (optional): Chip del perro.
    - **name** (required): Nombre del perro.
    - **about** (optional): Descripción del perro.
    - **age** (required): Edad del perro.
    - **is_vaccinated** (required): Indica si el perro esta vacunado. Debe ser un boolean:
        - **true**: El perro esta vacunado.
        - **false**: El perro no esta vacunado.
    - **image** (optional): Imagen del perro encriptad en base64.
    - **gender** (required): Genero del perro. Debe ser uno de los siguientes:
        - **male**: Representa un perro macho.
        - **female**: Representa un perro hembra.
    - **entry_date** (optional): Fecha de entrada en formato YYYY-MM-DD.
    - **is_sterilized** (required): Indica si el perro esta esterilizado. Debe ser un boolean:
        - **true**: El perro esta esterilizado.
        - **false**: El perro no esta esterilizado.
    - **is_dewormed** (required): Indica si el perro esta desparasitado. Debe ser un boolean:
        - **true**: El perro esta desparasitado.
        - **false**: El perro no esta desparasitado.
    - **operation** (optional): Especifica la/las operaciones del perro.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image_data = None
    if dog.image:
        try:
            image_data = base64.b64decode(dog.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")

    result = create_adoption_dog(db, dog, image_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Problema al crear")
    return result


@router.post('/adoption_dog/adopt/{dog_id}/{adoption_date}', response_model=dict)
def adopt_dog_by_id(dog_id: int, adoption_date: date, owner: OwnerCreate, db: Session = Depends(get_db),
                    current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Adopt a dog that is available for adoption:

    - **dog_id** (required): id of the adoption dog to be adopted.
    - **adoption_date** (required): Date of the adoption in format YYYY-MM-DD.

    - **name** (required): Name of the owner.
    - **direction** (required): Direction of the owner.
    - **cellphone** (required): Cellphone of the owner.

    Español:
    --------
    Adoptar a un perro que esté disponible para adopción:

    - **dog_id** (required): id del perro de adopción.
    - **adoption_date** (required): Fecha de la adopción en formatoYYYY-MM-DD.

    - **name** (required): Nombre del dueño.
    - **direction** (required): Dirección del dueño.
    - **cellphone** (required): Teléfono del dueño.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adoption_dog = read_adoption_dog_by_id(db, dog_id)

    if adoption_dog is None:
        raise HTTPException(status_code=404, detail="No existe")
    adopted_dog = adoption_dog.adopt(adoption_date, owner)
    result = create_owner_and_adopted_dog(db, adopted_dog)
    return result


@router.post('/adoption_dog/adopt/{dog_id}/{owner_id}/{adoption_date}', response_model=dict)
def adopt_dog_by_id_and_existing_owner(dog_id: int, adoption_date: date, owner_id: int,
                                       db: Session = Depends(get_db),
                                       current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Adopt a dog that is available for adoption:

    - **dog_id** (required): id of the adoption dog to be adopted.
    - **adoption_date** (required): Date of the adoption in format YYYY-MM-DD.
    - **owner_id** (required): Id of an existing owner.

    Español:
    --------
    Adoptar a un perro que esté disponible para adopción:

    - **dog_id** (required): id del perro de adopción.
    - **adoption_date** (required): Fecha de la adopción en formatoYYYY-MM-DD.
    - **owner_id** (required): Id de un Dueño existente.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adoption_dog = read_adoption_dog_by_id(db, dog_id)
    if adoption_dog is None:
        raise HTTPException(status_code=404, detail="Perro de adopción no existe")
    owner = read_owner_by_id(db, owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Dueño no existe")
    adopted_dog = adoption_dog.adopt_existing_owner(adoption_date, owner)
    result = adopt_dog(db, adopted_dog)
    return result


@router.get('/adoption_dog/', response_model=List[StaticDogResponse])
def get_adoption_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros dee adopcion.
    """
    adoption_dog = read_all_adoption_dogs(db)
    if not adoption_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros en adopcion")

    for dog in adoption_dog:
        if dog.image:
            dog.image = f'{API_URL}/dog/adoption_dog/{dog.id}/image'
        else:
            dog.image = None
    return adoption_dog


@router.get('/adoption_dog/{dog_id}', response_model=StaticDogResponse)
def get_adoption_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro de adopcion.
    """
    adoption_dog = read_adoption_dog_by_id(db, dog_id)
    if not adoption_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros de adopcion")
    if adoption_dog.image:
        adoption_dog.image = f'{API_URL}/dog/adoption_dog/{adoption_dog.id}/image'
    else:
        adoption_dog.image = None
    return adoption_dog


@router.get("/adoption_dog/{dog_id}/image", response_class=StreamingResponse)
def get_adoption_dog_image(dog_id: int, db: Session = Depends(get_db)):
    adoption_dog = read_adoption_dog_by_id(db, dog_id)
    if not adoption_dog or not adoption_dog.image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return StreamingResponse(io.BytesIO(adoption_dog.image), media_type="image/jpeg")


@router.put('/adoption_dog/update/{id_dog}', response_model=dict)
async def update_an_adoption_dog(id_dog: int,
                                 dog: AdoptionDogCreate,
                                 db: Session = Depends(get_db),
                                 current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update an adoption dog:

    - **id_chip** (optional): chip of the dog.
    - **name** (required): Name of the dog.
    - **about** (optional): Description of the dog.
    - **age** (required): Age of the dog.
    - **is_vaccinated** (required): Indicates if the dog is vaccinated. Must be a boolean:
        - **true**: The dog is vaccinated.
        - **false**: The dog is not vaccinated.
    - **image** (optional): Base64 encrypted image of the dog.
    - **gender** (required): Gender of the dog. Must be one of:
        - **male**: Represents a male dog.
        - **female**: Represents a female dog.
    - **entry_date** (optional): Date of the entry in format YYYY-MM-DD.
    - **is_sterilized** (required): Indicates if the dog is sterilized. Must be a boolean:
        - **true**: The dog is sterilized.
        - **false**: The dog is not sterilized
    - **is_dewormed** (required): Indicates if the dog is dewormed. Must be a boolean:
        - **true**: The dog is dewormed.
        - **false**: The dog is not dewormed
    - **operation** (optional): Specify the operation of the dog.
    Español:
    --------
    Actualizar un perro de adopción:

    - **id_chip** (optional): Chip del perro.
    - **name** (required): Nombre del perro.
    - **about** (optional): Descripción del perro.
    - **age** (required): Edad del perro.
    - **is_vaccinated** (required): Indica si el perro esta vacunado. Debe ser un boolean:
        - **true**: El perro esta vacunado.
        - **false**: El perro no esta vacunado.
    - **image** (optional): Imagen del perro encriptad en base64.
    - **gender** (required): Genero del perro. Debe ser uno de los siguientes:
        - **male**: Representa un perro macho.
        - **female**: Representa un perro hembra.
    - **entry_date** (optional): Fecha de entrada en formato YYYY-MM-DD.
    - **is_sterilized** (required): Indica si el perro esta esterilizado. Debe ser un boolean:
        - **true**: El perro esta esterilizado.
        - **false**: El perro no esta esterilizado.
    - **is_dewormed** (required): Indica si el perro esta desparasitado. Debe ser un boolean:
        - **true**: El perro esta desparasitado.
        - **false**: El perro no esta desparasitado.
    - **operation** (optional): Especifica la/las operaciones del perro.
    """
    # TODO validar en caso de que se actualice también el id
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if dog.image:
        try:
            image_data = base64.b64decode(dog.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    else:
        db_dogg = read_adoption_dog_by_id(db, id_dog)
        if db_dogg:
            image_data = db_dogg.image
        else:
            raise HTTPException(status_code=404, detail="Perro no encontrado")
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")
    # Crear el perro en la base de datos
    result = update_adoption_dog(db, dog, id_dog, image_data)
    if result is None:
        raise HTTPException(status_code=409, detail="Error al actualizar el perro")
    return result


@router.delete('/adoption_dog/delete/{id_adoption_dog}', response_model=dict)
def delete_adoption_dog_by_id(id_adoption_dog: int, db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para borrar un perro de adopcion.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dog_response = delete_an_adoption_dog_by_id(db, id_adoption_dog)
    if dog_response:
        return {"success": True, "message": "Perro de adopcion Borrado"}
    else:
        return {"success": False, "message": "Perro de adopcion no eliminado"}


@router.get('/adopted_dog/', response_model=List[AdoptedDogResponse])
def get_adopted_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros adoptados.
    """
    adopted_dogs = read_all_adopted_dogs(db)
    if not adopted_dogs:
        raise HTTPException(status_code=404, detail="No se encontraron perros adoptados")
    for dog in adopted_dogs:
        # Codificar la imagen en Base64 si existe
        if dog.image:
            dog.image = f'{API_URL}/dog/adopted_dog/{dog.id}/image'
    return adopted_dogs


@router.get('/adopted_dog/{dog_id}', response_model=AdoptedDogResponse)
def get_adopted_dog_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro adoptado.
    """
    adopted_dog = read_adopted_dogs_by_id(db, dog_id)
    if not adopted_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros adoptados")
    if adopted_dog.image:
        adopted_dog.image = f'{API_URL}/dog/adopted_dog/{adopted_dog.id}/image'
    return adopted_dog


@router.get("/adopted_dog/{dog_id}/image", response_class=StreamingResponse)
def get_adopted_dog_image(dog_id: int, db: Session = Depends(get_db)):
    adopted_dog = read_adopted_dogs_by_id(db, dog_id)
    if not adopted_dog or not adopted_dog.image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return StreamingResponse(io.BytesIO(adopted_dog.image), media_type="image/jpeg")


@router.put('/adopted_dog/update/{id_dog}', response_model=dict)
async def update_an_adopted_dog(id_dog: int,
                                dog: AdoptedDogUpdate,
                                db: Session = Depends(get_db),
                                current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update an adopted dog:

    - **id_chip** (optional): chip of the dog.
    - **name** (required): Name of the dog.
    - **about** (optional): Description of the dog.
    - **age** (required): Age of the dog.
    - **is_vaccinated** (required): Indicates if the dog is vaccinated. Must be a boolean:
        - **true**: The dog is vaccinated.
        - **false**: The dog is not vaccinated.
    - **image** (optional): Base64 encrypted image of the dog.
    - **gender** (required): Gender of the dog. Must be one of:
        - **male**: Represents a male dog.
        - **female**: Represents a female dog.
    - **entry_date** (optional): Date of the entry in format YYYY-MM-DD.
    - **is_sterilized** (required): Indicates if the dog is sterilized. Must be a boolean:
        - **true**: The dog is sterilized.
        - **false**: The dog is not sterilized
    - **is_dewormed** (required): Indicates if the dog is dewormed. Must be a boolean:
        - **true**: The dog is dewormed.
        - **false**: The dog is not dewormed
    - **operation** (optional): Specify the operation of the dog.
    Español:
    --------
    Actualizar un perro adoptado:

    - **id_chip** (optional): Chip del perro.
    - **name** (required): Nombre del perro.
    - **about** (optional): Descripción del perro.
    - **age** (required): Edad del perro.
    - **is_vaccinated** (required): Indica si el perro esta vacunado. Debe ser un boolean:
        - **true**: El perro esta vacunado.
        - **false**: El perro no esta vacunado.
    - **image** (optional): Imagen del perro encriptad en base64.
    - **gender** (required): Genero del perro. Debe ser uno de los siguientes:
        - **male**: Representa un perro macho.
        - **female**: Representa un perro hembra.
    - **entry_date** (optional): Fecha de entrada en formato YYYY-MM-DD.
    - **is_sterilized** (required): Indica si el perro esta esterilizado. Debe ser un boolean:
        - **true**: El perro esta esterilizado.
        - **false**: El perro no esta esterilizado.
    - **is_dewormed** (required): Indica si el perro esta desparasitado. Debe ser un boolean:
        - **true**: El perro esta desparasitado.
        - **false**: El perro no esta desparasitado.
    - **operation** (optional): Especifica la/las operaciones del perro.
    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if dog.image:
        try:
            image_data = base64.b64decode(dog.image)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid image encoding")
    else:
        db_dogg = read_adopted_dogs_by_id(db, id_dog)
        if db_dogg:
            image_data = db_dogg.image
        else:
            raise HTTPException(status_code=404, detail="Perro no encontrado")
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")
    # Crear el perro en la base de datos
    result = update_adopted_dog(db, dog, id_dog, image_data)
    if result is None:
        raise HTTPException(status_code=409, detail="Error al actualizar el perro")
    return result


@router.post('/adopted_dog/unadopt/{dog_id}/', response_model=dict)
def unadopt_dog_by_id(dog_id: int, db: Session = Depends(get_db),
                      current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adopted_dog = read_adopted_dogs_by_id(db, dog_id)
    result = un_adopt_dog_service(db, adopted_dog)
    return result
