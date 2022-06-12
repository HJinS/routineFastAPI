from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from commons.utils.jwt.jwt_handler import decode_jwt
from datetime import datetime
from typing import Tuple


class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid authentication scheme.')
            is_valid, is_expired = self.verify_jwt(credentials.credentials)
            if not is_valid and is_expired:
                raise HTTPException(status_code=403, detail='Expired token.')
            elif not is_valid and not is_expired:
                raise HTTPException(status_code=403, detail='Invalid token.')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail='Invalid authorization code.')

    @staticmethod
    def verify_jwt(jwt_token: str) -> Tuple[bool, bool]:
        is_token_valid: bool = False
        is_token_expired: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except:
            payload = None
        if payload:
            exp = payload['exp']
            type = payload['type']
            if exp < datetime.utcnow():
                is_token_expired = True
            elif type == 'access':
                is_token_valid = True
        return is_token_valid, is_token_expired
        