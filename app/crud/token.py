from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.domain.token import AuthToken


def create_token(db: Session, token: AuthToken):
    try:
        db.add(token)
        db.commit()
        db.refresh(token)
        return True
    except IntegrityError as ie:
        db.rollback()
        return False

# TODO: Implements Delete token and extend token(for expiration time)


