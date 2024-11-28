import base64
import io
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.dog import read_all_static_dogs, read_static_dogs_by_id, create_static_dog, delete_an_static_dog_by_id, \
    read_all_adoption_dogs, read_adoption_dog_by_id, create_adoption_dog, delete_an_adoption_dog_by_id, \
    read_all_adopted_dogs, read_adopted_dogs_by_id, unadopt_dog, update_static_dog, update_adoption_dog
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.dog import StaticDogResponse, StaticDogCreate, AdoptionDogResponse, AdoptionDogCreate, \
    AdoptedDogResponse
from app.models.schema.owner import OwnerCreate, OwnerResponse
from app.models.schema.user import TokenData
from app.services.images_control_service import verify_image_size
from app.services.password import create_owner_and_adopted_dog

router = APIRouter()


@router.post('/static_dog/create/', response_model=dict)
async def create_new_static_dog(dog: StaticDogCreate,
                                db: Session = Depends(get_db),
                                current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Create a static dog:

    - **id** (required): id of the dog.
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

    Español:
    --------
    Crear un perro estático:

    - **id** (required): id del perro.
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
    dog_list = []
    for dog in static_dogs:
        # Codificar la imagen en Base64 si existe
        image_base64 = base64.b64encode(dog.image).decode('utf-8') if dog.image else None
        dog_data = StaticDogResponse(
            id=dog.id,
            name=dog.name,
            about=dog.about,
            age=dog.age,
            is_vaccinated=dog.is_vaccinated,
            gender=dog.gender,
            image=image_base64,
            entry_date=dog.entry_date,
            is_sterilized=dog.is_sterilized,
            is_dewormed=dog.is_dewormed,
            operation=dog.operation
        )
        dog_list.append(dog_data)
    return dog_list


@router.get('/static_dog/{dog_id}', response_model=StaticDogResponse)
def get_static_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    static_dog = read_static_dogs_by_id(db, dog_id)

    if not static_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros estáticos")
    # noinspection PyTypeChecker
    static_dog.image = base64.b64encode(static_dog.image).decode('utf-8') if static_dog.image else None
    return static_dog


@router.get("/static_dog/{dog_id}/imagen", response_class=StreamingResponse)
async def get_imagen_perro_grande(dog_id: int, db: Session = Depends(get_db)):
    static_dog = get_static_dogs_by_id(db, dog_id)
    if not static_dog or not static_dog.image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return StreamingResponse(io.BytesIO(static_dog.imagen), media_type="image/jpeg")


@router.put('/static_dog/update/', response_model=dict)
async def update_a_static_dog(dog: StaticDogCreate,
                              db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update a static dog:

    - **id** (required): id of the dog.
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

    Español:
    --------
    Actualizar un perro estático:

    - **id** (required): id del perro.
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
        image_data = read_static_dogs_by_id(db, dog.id).image
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")
    # Crear el perro en la base de datos
    result = update_static_dog(db, dog, image_data)
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

    - **id** (required): id of the dog.
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

    Español:
    --------
    Crear un perro de adopción:

    - **id** (required): id del perro.
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


@router.get('/adoption_dog/', response_model=List[StaticDogResponse])
def get_adoption_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros dee adopcion.
    """
    adoption_dog = read_all_adoption_dogs(db)
    if not adoption_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros en adopcion")
    adoption_dog_list = []

    for dog in adoption_dog:
        # Codificar la imagen en Base64 si existe
        image_base64 = base64.b64encode(dog.image).decode('utf-8') if dog.image else None
        dog_data = AdoptionDogResponse(
            id=dog.id,
            name=dog.name,
            about=dog.about,
            age=dog.age,
            is_vaccinated=dog.is_vaccinated,
            gender=dog.gender,
            image=image_base64,
            entry_date=dog.entry_date,
            is_sterilized=dog.is_sterilized,
            is_dewormed=dog.is_dewormed,
            operation=dog.operation
        )
        adoption_dog_list.append(dog_data)
    return adoption_dog_list


@router.get('/adoption_dog/{dog_id}', response_model=StaticDogResponse)
def get_adoption_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro de adopcion.
    """
    adoption_dog = read_adoption_dog_by_id(db, dog_id)
    if not adoption_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros de adopcion")
    adoption_dog.image = base64.b64encode(adoption_dog.image).decode('utf-8') if adoption_dog.image else None
    return adoption_dog


@router.put('/adoption_dog/update/', response_model=dict)
async def update_an_adoption_dog(dog: AdoptionDogCreate,
                                 db: Session = Depends(get_db),
                                 current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Update a static dog:

    - **id** (required): id of the dog.
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

    Español:
    --------
    Actualizar un perro estático:

    - **id** (required): id del perro.
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
        :param dog:
        :param db:
        :param current_user:
        :return:
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
        image_data = read_adoption_dog_by_id(db, dog.id).image
    # verificamos el tamaño de la imagen
    if image_data:
        try:
            verify_image_size(image_data)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image size")
    # Crear el perro en la base de datos
    result = update_adoption_dog(db, dog, image_data)
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

    adopted_dogs_list = []
    for dog in adopted_dogs:
        # Codificar la imagen en Base64 si existe
        image_base64 = base64.b64encode(dog.image).decode('utf-8') if dog.image else None

        owner_data = OwnerResponse(
            id=dog.owner.id,
            name=dog.owner.name,
            direction=dog.owner.direction,
            cellphone=dog.owner.cellphone
        )

        # Crear el objeto de respuesta AdoptedDogResponse
        dog_data = AdoptedDogResponse(
            id=dog.id,
            name=dog.name,
            about=dog.about,
            age=dog.age,
            is_vaccinated=dog.is_vaccinated,
            gender=dog.gender,
            image=image_base64,
            entry_date=dog.entry_date,
            is_sterilized=dog.is_sterilized,
            is_dewormed=dog.is_dewormed,
            operation=dog.operation,
            adopted_date=dog.adopted_date,
            owner=owner_data
        )
        adopted_dogs_list.append(dog_data)

    return adopted_dogs_list


@router.get('/adopted_dog/{dog_id}', response_model=AdoptedDogResponse)
def get_adopted_dog_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro adoptado.
    """
    adopted_dog = read_adopted_dogs_by_id(db, dog_id)
    if not adopted_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros adoptados")
    print(adopted_dog.image)
    adopted_dog.image = base64.b64encode(adopted_dog.image).decode('utf-8') if adopted_dog.image else None
    return adopted_dog


@router.post('/adopted_dog/unadopt/{dog_id}/', response_model=dict)
def unadopt_dog_by_id(dog_id: int, db: Session = Depends(get_db),
                      current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adopted_dog = read_adopted_dogs_by_id(db, dog_id)
    if adopted_dog is None:
        raise HTTPException(status_code=404, detail="No existe")
    adoption_dog = adopted_dog.unadopt()
    result = unadopt_dog(db, adoption_dog, adopted_dog.owner.id)
    return result
