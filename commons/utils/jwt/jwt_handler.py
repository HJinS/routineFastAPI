import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
from typing import Dict

load_dotenv('../../config/.env')

JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']


class JWTToken:

    def __init__(self, email):
        self.payload = {
            'email': email,
        }

    def __generate_token(self):
        self.payload['iat'] = datetime.utcnow()
        token = jwt.encode(self.payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @property
    def access_token(self):
        self.payload['type'] = 'access'
        self.payload['exp'] = datetime.utcnow() + timedelta(hours=3)
        return self.__generate_token()

    @property
    def refresh_token(self):
        self.payload['type'] = 'refresh'
        self.payload['exp'] = datetime.utcnow() + timedelta(days=5)
        return self.__generate_token()


def token_response(access_token: str, refresh_token: str):
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def sign_jwt(email: str) -> Dict[str, str]:
    jwt_token = JWTToken(email)
    access_token = jwt_token.access_token
    refresh_token = jwt_token.refresh_token
    return token_response(access_token, refresh_token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return {}
