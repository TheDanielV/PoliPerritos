from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import relationship

from app.db.database import Base

applicant_course = Table(
    'applicant_course', Base.metadata,
    Column('applicant_id', Integer, ForeignKey('applicant.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)


class Applicant(Base):
    __tablename__ = "applicant"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    cellphone = Column(String(255), nullable=False)
    image = Column(LONGBLOB, nullable=False)

    # Relación muchos a muchos con Course
    course = relationship(
        "Course",
        secondary=applicant_course,
        back_populates="applicant"
    )