from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.domain.dog import AdoptedDog


class Visit(Base):
    __tablename__ = "visit"
    id = Column(Integer, primary_key=True, index=True)
    visit_date = Column(Date, nullable=False)
    evidence = Column(LONGBLOB, nullable=True)
    observations = Column(String(length=255), nullable=True)
    adopted_dog_id = Column(Integer, ForeignKey('adopted_dogs.id'), nullable=False)
    adopted_dog = relationship('AdoptedDog', back_populates='visits')
