from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .models import UserTable
from commons.config.db import session_scope
from .schemas import UserRegistrationSchema, UserLoginSchema
from commons.utils.jwt.jwt_handler import sign_jwt

user_app = FastAPI()


@user_app.post('/register')
def register(user_register: UserRegistrationSchema):
    with session_scope() as session:
        user_obj = UserTable(email=user_register.email, first_name=user_register.first_name, last_name=user_register.last_name, password=user_register.password)
        session.add(user_obj)
        session.commit()
    return sign_jwt(user_register.email)


@user_app.post('/login')
def login(user_login: UserLoginSchema):
    if check_user(user_login):
        return sign_jwt(user_login.email)
    else:
        return JSONResponse(content={'Error': 'Wrong user credential'}, status_code=403)


def check_user(user: UserLoginSchema):
    with session_scope() as session:
        if session.query(UserTable).filter(UserTable.email == user.email and UserTable.password == user.password):
            return True
        else:
            return False
