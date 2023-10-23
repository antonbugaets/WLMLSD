from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserInfoResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    total_created: int


class StatusResponse(BaseModel):
    task_id: str
    status: str
    state: str
    result: str
