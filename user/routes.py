from models import UserTable
from commons.config.db import session_scope
from schemas import UserSchema
from fastapi import APIRouter

user = APIRouter()


@user.post('/register')
def register(user_in: UserSchema):
    with session_scope() as session:
        user_obj = UserTable(email=user_in.email, first_name=user_in.first_name, last_name=user_in.last_name, password=user_in.password)
        session.add(user_obj)
        session.commit()
    return {''}
