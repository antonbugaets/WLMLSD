import logging

from api_src.api.actions.users import (
    create_new_user,
    get_current_user,
    authenticate_by_login_password,
)
from api_src.db.session import get_db
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api_src.api import pydantic_models as models
from api_src.core.security import create_access_token

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    path="/signup",
    tags=["Authorisation / Registration"],
    description="User registration via email and password.",
)
async def create_user(
    request: Request,
    body: models.UserRegisterRequest,
    session: AsyncSession = Depends(get_db),
) -> models.UserLoginResponse:
    access_token, user_id = await create_new_user(body, session)

    return models.UserLoginResponse(access_token=access_token, token_type="bearer")


@router.post(
    path="/login",
    tags=["Authorisation / Registration"],
    description="OAuth 2.0 auth via login (e-mail) and password.",
    response_model=models.UserLoginResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> models.UserLoginResponse:
    access_token = await authenticate_by_login_password(
        form_data.username, form_data.password, session
    )

    return models.UserLoginResponse(access_token=access_token, token_type="bearer")


@router.get(
    path="/me/",
    tags=["Authorisation / Registration"],
    description="Returns current user by JWT token.",
    response_model=models.UserInfoResponse,
)
async def read_users_me(
    current_user: models.UserInfoResponse = Depends(get_current_user),
) -> models.UserInfoResponse:
    return current_user


@router.get(
    path="/refresh_token",
    tags=["Authorisation / Registration"],
    description="Returns new JWT token.",
    response_model=models.UserLoginResponse,
)
async def refresh_token(
    current_user: models.UserInfoResponse = Depends(get_current_user),
) -> models.UserLoginResponse:
    access_token = create_access_token(
        data={"email": current_user.email, "aim": "login"}
    )

    return models.UserLoginResponse(access_token=access_token, token_type="bearer")
