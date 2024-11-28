from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.core.security import create_auth_user
from app.db.database import SessionLocal
from app.models.domain.user import Role, User
from app.models.schema.user import UserCreate


def create_admin_user():
    db = SessionLocal()
    try:
        admin = db.query(User).filter_by(role="admin").first()
        if not admin:
            auth_user = UserCreate(username=settings.ADMIN_USERNAME,
                                   email=settings.ADMIN_EMAIL,
                                   password=settings.ADMIN_PASSWORD,
                                   role=Role.ADMIN)
            create_auth_user(db, auth_user)
    finally:
        db.close()
