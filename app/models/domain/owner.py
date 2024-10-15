# app/models/domain/owner.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.database import Base


# Se crea el modelo paara un usuario
class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    direction = Column(String(255), index=True, nullable=False)
    cellphone = Column(Integer, nullable=False)
    adopted_dogs = relationship("AdoptedDog", back_populates="owner")
