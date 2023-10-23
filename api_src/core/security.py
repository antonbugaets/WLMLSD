import os
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi.exceptions import HTTPException

from api_src.api.exceptions import credentials_exception

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
EMAIL_CODE_EXPIRE_MINUTES = float(os.getenv("EMAIL_CODE_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict, email=False):
    if not email:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        access_token_expires = timedelta(minutes=EMAIL_CODE_EXPIRE_MINUTES)

    to_encode = data.copy()

    expire = datetime.utcnow() + access_token_expires

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        aim: str = payload.get("aim")
        if email is None or aim is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has been expired")
    except JWTError:
        raise credentials_exception

    return email, aim
