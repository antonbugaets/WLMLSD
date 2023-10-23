import logging

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_src.api import pydantic_models as models
from api_src.api.exceptions import credentials_exception
from api_src.core.hashing import Hasher
from api_src.core.security import create_access_token
from api_src.core.security import decode_access_token, oauth2_scheme
from api_src.db.dals.users import UserDAL
from api_src.db.session import get_db

logger = logging.getLogger(__name__)


async def create_new_user(body: models.UserRegisterRequest, session):
    async with session.begin():
        user_dal = UserDAL(session)

        exists = await user_dal.get_user_by_email(body.email)
        if exists is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {body.email} already exists",
            )

        user = await user_dal.create_user(
            name=body.name,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )

    token = create_access_token(data={"email": user.email, "aim": "login"})

    return token, user.user_id


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
):
    email, aim = decode_access_token(token)

    if aim != "login":
        raise credentials_exception

    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email)

        if user is None:
            raise credentials_exception

        user_info = models.UserInfoResponse(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            total_created=user.total_created,
        )

    return user_info


async def authenticate_by_login_password(username: str, password: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.authenticate_user(email=username, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token = create_access_token(data={"email": user.email, "aim": "login"})

    return access_token