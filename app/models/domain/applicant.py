from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.services.crypt import encrypt_str_data, encrypt_image, decrypt_str_data, decrypt_image


class Applicant(Base):
    __tablename__ = "applicant"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    cellphone = Column(String(255), nullable=False)
    image = Column(LONGBLOB, nullable=False)

    # Relación muchos a muchos con Course
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    course = relationship('Course', back_populates='applicant')

    def crypt_data(self):
        self.first_name = encrypt_str_data(self.first_name)
        self.last_name = encrypt_str_data(self.last_name)
        self.email = encrypt_str_data(self.email)
        self.cellphone = encrypt_str_data(self.cellphone)
        self.image = encrypt_image(self.image)
        print(f'nombre encriptado: {self.first_name}')

    def decrypt_data(self):

        self.first_name = decrypt_str_data(self.first_name)
        self.last_name = decrypt_str_data(self.last_name)
        self.email = decrypt_str_data(self.email)
        self.cellphone = decrypt_str_data(self.cellphone)
        self.image = decrypt_image(self.image)

