from sqlalchemy import Column, String
from sqlalchemy_utils import PasswordType
import uuid

from commons.config.db import Base


class UserTable(Base):

    __tablename__: str = 'user'
    id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(25), unique=True)
    first_name = Column(String(15))
    last_name = Column(String(15))
    password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecdated=['md5_crypt']))
