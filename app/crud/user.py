from sqlalchemy.orm import Session

from app.models.domain.user import User


def get_user_id_by_email(db: Session, user_email: str):
    """
    Devuelve el id de un usuario con base en su email.
    """
    user = db.query(User).filter(User.email == user_email).first()
    if user:
        return user.id
    else:
        return None
