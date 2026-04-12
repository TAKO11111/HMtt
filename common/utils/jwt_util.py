#加密和解码token的工具
import jwt
from flask import current_app
def generate_jwt(payload,expiry,secret):
    _payload={"exp":expiry}
    _payload.update(payload)
    if not secret:
        secret=current_app.config['JWT_SECRET']
    token=jwt.encode(_payload,secret,algorithm='HS256')
    return token

def verify(token,secret=None):
    if not secret:
        secret=current_app.config['JWT_SECRET']

    try:
        payload=jwt.decode(token,secret,algorithms=['HS256'])
    except jwt.PyJWTError:
        payload=None
    return payload