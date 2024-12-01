from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.user import User
from app.models.schema.user import UserCreate, UserUpdate
from app.services.crypt import get_password_hash, verify_password


def create_auth_user(db: Session, user: UserCreate):
    db_auth_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
        role=user.role,
        is_active=False
    )
    try:
        db.add(db_auth_user)
        db.commit()
        db.refresh(db_auth_user)
        return {"detail": "Usuario creado"}
    except IntegrityError as ie:
        db.rollback()
        error_message = str(ie.orig)

        if "Duplicate entry" in error_message:
            if "username" in error_message:
                raise HTTPException(
                    status_code=400, detail="El username ya está en uso."
                )
            elif "email" in error_message:
                raise HTTPException(
                    status_code=400, detail="El email ya está en uso."
                )
        raise HTTPException(
            status_code=500, detail="Error al actualizar el usuario. Por favor, inténtelo nuevamente."
        )


def get_user_id_by_email(db: Session, user_email: str):
    """
    Devuelve el id de un usuario con base en su email.
    """
    user = db.query(User).filter(User.email == user_email).first()
    if user:
        return user.id
    else:
        return None


def get_user_id_by_id(db: Session, user_id: int):
    """
        Devuelve el id de un usuario con base en su email.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_password(db: Session, user_id: int, new_password: str):
    user = get_user_id_by_id(db, user_id)

    if user:
        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        return user


def update_auth_user_basic_information(db: Session, user: UserUpdate, actual_username: str):
    db_user = db.query(User).filter(User.username == actual_username).first()
    if user.username != db_user.username and user.username:
        db_user.username = user.username
    if user.email != db_user.email and user.email:
        db_user.email = user.email
    try:
        db.merge(db_user)
        db.commit()
        db.refresh(db_user)
        return {"detail": "Información Actualizada"}
    except IntegrityError as ie:
        db.rollback()
        error_message = str(ie.orig)
        if "Duplicate entry" in error_message:
            if "username" in error_message:
                raise HTTPException(
                    status_code=400, detail="El username ya está en uso."
                )
            elif "email" in error_message:
                raise HTTPException(
                    status_code=400, detail="El email ya está en uso."
                )
        raise HTTPException(
            status_code=500, detail="Error al actualizar el usuario. Por favor, inténtelo nuevamente."
        )


def update_auth_user_password(db: Session, current_user_username: str, actual_password: str, new_password: str):
    db_user = db.query(User).filter(User.username == current_user_username).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario no encontrado."
        )
    if not verify_password(actual_password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Contraseña actual incorrecta."
        )
    try:
        db_user.hashed_password = get_password_hash(new_password)
        db.add(db_user)
        db.commit()
        return {"detail": "Contraseña Actualizada"}
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error, intentalo más tarde"
        )


def delete_auth_user(db: Session, user_id: int, current_user_username: str):
    """
    Deletes a user by their ID.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.
        current_user_username (str): Username of the current user.

    Raises:
        HTTPException: Raised with appropriate status codes and messages.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado."
        )
    if user.username == current_user_username:
        raise HTTPException(
            status_code=403, detail="No se puede eliminar el usuario actual."
        )
    else:
        try:
            db.delete(user)
            db.commit()
            return {"success": True, "message": "Usuario eliminado"}
        except IntegrityError as ie:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=ie
            )
