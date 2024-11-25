# app/models/domain/token.py
import random
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class AuthToken(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    value = Column(String(255), unique=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_expiration = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)

    # Relación con Usuario
    user = relationship("User", back_populates="token")

    def generate_token(self, user_id):
        """Crea un nuevo token para un usuario."""
        self.user_id = user_id
        self.value = random.randint(100000, 999999)
        self.date_creation = datetime.utcnow()
        self.date_expiration = datetime.utcnow() + timedelta(minutes=5)
        self.is_used = False

    def use_token(self):
        if self.value and self.user_id:
            self.is_used = True
        if self.date_expiration > datetime.now() and self.value and self.user_id:
            self.is_used = True
