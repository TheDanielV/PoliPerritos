# app/models/domain/owner.py
from sqlalchemy import Column, Integer, String, Text, Date, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


# Se crea el modelo paara un usuario
class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    schedule = relationship("Schedule", back_populates="course", cascade="all, delete-orphan")
    applicant = relationship('Applicant', back_populates='course', cascade='all, delete-orphan')  # Relación con Applicant

