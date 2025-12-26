import jwt
from settings.settings import Settings
from datetime import timedelta, datetime

def create_access_token(data: dict) -> str:

    payload = {
        'sub': data['sub'],
        'user_id': data['user_id'],
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=Settings().JWT_EXCPIRE_MINUTE),
        'iat': datetime.utcnow()
    }

    return jwt.encode(
        payload, Settings().JWT_SECRET_KEY, algorithm=Settings().JWT_ALGO
    )

def create_refresh_token(data: dict) -> str:

    payload = {
        'sub': data['sub'],
        'user_id': data['user_id'],
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }

    return jwt.encode(
        payload, Settings().JWT_SECRET_KEY, algorithm=Settings().JWT_ALGO
    )


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, Settings().JWT_SECRET_KEY, algorithms=[Settings().JWT_ALGO])
    except jwt.ExpiredSignatureError as e:
        return e
    except jwt.InvalidTokenError as e:
        return e