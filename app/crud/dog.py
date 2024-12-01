# Poliperritos/app/crud/dog.py
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import Session

from app.crud.owner import read_owner_by_id
from app.models.domain.dog import *
from app.models.schema.dog import *


# Crud 4 Static Dogs
def create_static_dog(db: Session, static_dog: StaticDogCreate, image: bytes = None):
    """
       Crea y guarda un perro estático en la base de datos.

       Esta función registra un perro estático en la base de datos utilizando los datos proporcionados.
       Opcionalmente, permite asociar una imagen en formato binario (bytes) al registro del perro.

       Parameters:
       ----------
       - db (Session):
           Una instancia de la sesión de base de datos proporcionada por SQLAlchemy.
       - static_dog (StaticDogCreate):
           Un objeto que contiene los datos del perro estático, incluyendo:
               - `id` (int): Identificador único del perro.
               - `name` (str): Nombre del perro.
               - `about` (str): Descripción breve sobre el perro.
               - `age` (int): Edad del perro en años.
               - `is_vaccinated` (bool): Indica si el perro está vacunado.
               - `gender` (str): Género del perro (por ejemplo, "Macho", "Hembra").
       - image (bytes, optional):
           Una imagen asociada al perro, representada en formato binario. Por defecto, es `None`.

       Returns:
       --------
       - dict:
           Retorna un diccionario con un mensaje de éxito, como:
           `{"detail": "Perro Permanente creado"}` si el registro fue creado exitosamente.
       - None:
           Retorna `None` si ocurre un error de integridad, como un conflicto de clave única.

       Exceptions:
       -----------
       - IntegrityError:
           Si se encuentra un conflicto de clave única u otro error de integridad en la base de datos,
           la función revierte la transacción y retorna `None`.

       Example:
       --------
       Crear un nuevo perro estático en la base de datos:
       ```
       new_dog = StaticDogCreate(
           id=1,
           name="Firulais",
           about="Un perro juguetón",
           age=3,
           is_vaccinated=True,
           gender="male",
       )
       result = create_static_dog(db, new_dog, image=b'...')
       print(result) # {"detail": "Perro Permanente creado"}
       ```
       """

    db_static_dog = StaticDog(
        id_chip=static_dog.id_chip,
        name=static_dog.name,
        about=static_dog.about,
        age=static_dog.age,
        is_vaccinated=static_dog.is_vaccinated,
        gender=static_dog.gender,
        image=image,
        entry_date=static_dog.entry_date,
        is_sterilized=static_dog.is_sterilized,
        is_dewormed=static_dog.is_dewormed,
        operation=static_dog.operation
    )
    try:
        db.add(db_static_dog)
        db.commit()
        return {"detail": "Perro Permanente creado"}
    except IntegrityError:

        db.rollback()
        return None


def read_all_static_dogs(db: Session):
    """
     Devuelve una lista de perros estáticos existentes.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.

     Returns:

     Example:
     ```
     ```
     """
    return db.query(StaticDog).all()


def read_static_dogs_by_id(db: Session, dog_id: int) -> StaticDog:
    """
    Devuelve un perro estatico por su id.
    """
    return db.query(StaticDog).filter(StaticDog.id == dog_id).first()


def update_static_dog(db: Session, static_dog: StaticDogCreate, image: bytes = None):
    """
    """
    db_static_dog_update = StaticDog(
        id=static_dog.id,
        name=static_dog.name,
        about=static_dog.about,
        age=static_dog.age,
        is_vaccinated=static_dog.is_vaccinated,
        gender=static_dog.gender,
        image=image,
        entry_date=static_dog.entry_date,
        is_sterilized=static_dog.is_sterilized,
        is_dewormed=static_dog.is_dewormed,
        operation=static_dog.operation
    )
    try:
        db.merge(db_static_dog_update)
        db.commit()
        return {"detail": "Perro Permanente Actualizado"}
    except IntegrityError:
        db.rollback()
        return None


def delete_an_static_dog_by_id(db: Session, dog_id: int):
    """
    Elimina un perro estatico por su id.
    """
    dog = db.query(StaticDog).filter(StaticDog.id == dog_id).first()
    if dog is None:
        return False
    else:
        try:
            db.delete(dog)
            db.commit()
        except IntegrityError:
            db.rollback()  # Deshacer los cambios en caso de error
            return False
        return True


# Crud 4 adoption Dogs
def create_adoption_dog(db: Session, adoption_dog: AdoptionDogCreate, image: bytes = None):
    """
     Crea y guarda un perro de adopción en la base de datos.

     Parameters:
     - db (Session): La sesión de base de datos de SQLAlchemy.
     - static_dog (AdoptionDogCreate): Un objeto con los datos del perro de adopción, incluyendo nombre,
       descripción, edad, estado de vacunación, e imagen.
     - image (bytes): Imagen transformada en bytes.

     Returns:
     - Dict[str, str]: Un diccionario con un mensaje de éxito si el perro fue creado exitosamente.
     - None: Si ocurre un error de integridad (por ejemplo, un ID duplicado), devuelve `None`.

     Exceptions:
     - IntegrityError: Si ocurre un error de integridad, como un conflicto de clave única.

     Example:
     ```
     new_dog = AdoptionDog(
         id=1,
         name="Firulais",
         about="Un perro juguetón",
         age=3,
         is_vaccinated=True,
         image=b'...'
     )
     result = create_static_dog(db, new_dog)
     ```
     """
    db_adoption_dog = AdoptionDog(
        id=adoption_dog.id,
        name=adoption_dog.name,
        about=adoption_dog.about,
        age=adoption_dog.age,
        is_vaccinated=adoption_dog.is_vaccinated,
        gender=adoption_dog.gender,
        image=image,
        entry_date=adoption_dog.entry_date,
        is_sterilized=adoption_dog.is_sterilized,
        is_dewormed=adoption_dog.is_dewormed,
        operation=adoption_dog.operation
    )
    try:
        db.add(db_adoption_dog)
        db.commit()
        return {"detail": "Perro de adopcion creado"}
    except IntegrityError:
        db.rollback()
        return None
    except InvalidRequestError:
        db.rollback()
        return None


def read_all_adoption_dogs(db: Session):
    """
    Devuelve una lista de todos los perros para adopcion en la base de datos.
    :rtype: List[AdoptionDog]
    :param db:
    :return:
    """
    return db.query(AdoptionDog).all()


def read_adoption_dog_by_id(db: Session, dog_id: int):
    """
    Devuelve un perro de adopcion por su id.
    :rtype: AdoptionDog
    :param db:
    :param dog_id:
    :return:
    """
    return db.query(AdoptionDog).filter(AdoptionDog.id == dog_id).first()


def update_adoption_dog(db: Session, static_dog: AdoptionDogCreate, image: bytes = None):
    """
    """
    db_adoption_dog_update = AdoptionDog(
        id=static_dog.id,
        name=static_dog.name,
        about=static_dog.about,
        age=static_dog.age,
        is_vaccinated=static_dog.is_vaccinated,
        gender=static_dog.gender,
        image=image,
        entry_date=static_dog.entry_date,
        is_sterilized=static_dog.is_sterilized,
        is_dewormed=static_dog.is_dewormed,
        operation=static_dog.operation
    )
    try:
        db.merge(db_adoption_dog_update)
        db.commit()
        return {"detail": "Perro de Adopción Actualizado"}
    except IntegrityError:
        db.rollback()
        return None


def delete_an_adoption_dog_by_id(db: Session, dog_id: int):
    # Obtener el objeto a eliminar
    dog = db.query(AdoptionDog).filter(AdoptionDog.id == dog_id).first()
    if dog is None:
        return False
    else:
        try:
            db.delete(dog)
            db.commit()
        except IntegrityError:
            db.rollback()  # Deshacer los cambios en caso de error
            return False
        return True


def adopt_dog(db: Session, adopted_dog: AdoptedDog):
    adoption_dog = read_adoption_dog_by_id(db, adopted_dog.id)
    try:
        db.add(adopted_dog)
        db.add(adopted_dog.owner)
        db.delete(adoption_dog)
        db.commit()
        return {"detail": "Perro Adoptado creado"}
    except IntegrityError:
        db.rollback()
        return None


def create_adopted_dog_without_commit(db: Session, adopted_dog: AdoptedDog):
    adoption_dog = read_adoption_dog_by_id(db, adopted_dog.id)
    if adoption_dog:
        db.add(adopted_dog)
        db.delete(adoption_dog)
    return adoption_dog


def read_all_adopted_dogs(db: Session):
    """
    Devuelve una lista de todos los perros adoptados en la base de datos.
    """
    dogs = db.query(AdoptedDog).all()
    for dog in dogs:
        dog.owner.decrypt_data()
    return dogs


def read_adopted_dogs_by_id(db: Session, dog_id: int) -> AdoptedDog:
    """
    Devuelve un perro adoptado por id.
    """
    dog = db.query(AdoptedDog).filter(AdoptedDog.id == dog_id).first()

    if dog:
        dog.owner.decrypt_data()
    return dog


def unadopt_dog(db: Session, adoption_dog: AdoptionDog):

    dog = db.query(AdoptedDog).filter(AdoptedDog.id == adoption_dog.id).first()
    try:
        db.add(adoption_dog)
        if dog is not None:
            db.delete(dog)
        db.commit()
        return {"detail": "Perro des adoptado"}
    except IntegrityError:
        db.rollback()
        return None
