# app/models/domain/owner.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.services.crypt import decrypt_str_data, encrypt_str_data


# Se crea el modelo paara un usuario
class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    direction = Column(String(255), nullable=False)
    cellphone = Column(String(255), nullable=False)
    # Relación uno a muchos con AdoptedDog
    adopted_dogs = relationship("AdoptedDog", back_populates="owner", cascade="all, delete-orphan")

    def crypt_data(self):
        self.direction = encrypt_str_data(self.direction)
        self.cellphone = encrypt_str_data(self.cellphone)

    def decrypt_data(self):
        self.direction =  decrypt_str_data(self.direction)
        self.cellphone = decrypt_str_data(self.cellphone)