from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.dog import *
from app.crud.owner import *
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.schema.user import TokenData
from app.models.domain.user import Role

router = APIRouter()


@router.get('/static_dog/', response_model=List[StaticDogResponse])
def read_static_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros estáticos.
    """
    static_dogs = get_all_static_dogs(db)
    if not static_dogs:
        raise HTTPException(status_code=404, detail="No se encontraron perros estáticos")
    return static_dogs


@router.get('/static_dog/{dog_id}', response_model=StaticDogResponse)
def read_static_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro estático.
    """
    static_dog = get_static_dogs_by_id(db, dog_id)
    if not static_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros estáticos")
    return static_dog


@router.post('/static_dog/create/', response_model=dict)
def create_new_static_dog(dog: StaticDogCreate, db: Session = Depends(get_db),
                          current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para ocrear un perro estatico.
    """
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = create_static_dog(db, dog)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result


@router.delete('/static_dog/delete/{id_static_dog}', response_model=dict)
def delete_static_dog_by_id(id_static_dog: int, db: Session = Depends(get_db),
                            current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para borrar un perro estatico.
    """
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dog_response = delete_an_static_dog_by_id(db, id_static_dog)
    if dog_response:
        return {"success": True, "message": "Perro Permanente Borrado"}
    else:
        return {"success": False, "message": "Perro Permanente no eliminado"}


# 4 Adoption dog

@router.get('/adoption_dog/', response_model=List[StaticDogResponse])
def read_adoption_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros dee adopcion.
    """
    adoption_dog = get_all_adoption_dogs(db)
    if not adoption_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros de adopcion")
    return adoption_dog


@router.get('/adoption_dog/{dog_id}', response_model=StaticDogResponse)
def read_adoption_dogs_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro de adopcion.
    """
    static_dog = get_adoption_dog_by_id(db, dog_id)
    if not static_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros de adopcion")
    return static_dog


@router.post('/adoption_dog/create/', response_model=dict)
def create_new_adoption_dog(dog: AdoptionDogCreate, db: Session = Depends(get_db),
                            current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para ocrear un perro de adopcion.
    """
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = create_adoption_dog(db, dog)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result


@router.post('/adoption_dog/adopt/{dog_id}/{adoption_date}', response_model=dict)
def adopt_dog_by_id(dog_id: int, adoption_date: date, owner: OwnerCreate, db: Session = Depends(get_db),
                    current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adoption_dog = get_adoption_dog_by_id(db, dog_id)
    print(adoption_dog.name)
    adopted_dog = adoption_dog.adopt(adoption_date, owner)
    print(adopted_dog.owner.name)
    result = adopt_dog(db, adopted_dog)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result


@router.delete('/adoption_dog/delete/{id_adoption_dog}', response_model=dict)
def delete_adoption_dog_by_id(id_adoption_dog: int, db: Session = Depends(get_db),
                              current_user: TokenData = Depends(get_current_user)):
    """
    Endpoint para borrar un perro de adopcion.
    """
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    dog_response = delete_an_adoption_dog_by_id(db, id_adoption_dog)
    if dog_response:
        return {"success": True, "message": "Perro de adopcion Borrado"}
    else:
        return {"success": False, "message": "Perro de adopcion no eliminado"}


@router.get('/adopted_dog/', response_model=List[AdoptedDogResponse])
def read_adopted_dogs(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los perros adoptados.
    """
    adopted_dogs = get_all_adopted_dogs(db)
    if not adopted_dogs:
        raise HTTPException(status_code=404, detail="No se encontraron perros adoptados")
    return adopted_dogs


@router.get('/adopted_dog/{dog_id}', response_model=AdoptedDogResponse)
def read_adopted_dog_by_id(dog_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un perro adoptado.
    """
    adopted_dog = get_adopted_dogs_by_id(db, dog_id)
    if not adopted_dog:
        raise HTTPException(status_code=404, detail="No se encontraron perros adoptados")
    return adopted_dog

@router.post('/adopted_dog/unadopt/{dog_id}/', response_model=dict)
def unadopt_dog_by_id(dog_id: int, db: Session = Depends(get_db),
                      current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in Role._value2member_map_:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    adopted_dog = get_adopted_dogs_by_id(db, dog_id)
    adoption_dog = adopted_dog.unadopt()
    result = unadopt_dog(db, adoption_dog, adopted_dog.owner.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result
