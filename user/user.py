from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import PasswordType
import uuid

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(15))
    last_name = Column(String(15))
    password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecdated=['md5_crypt']))

