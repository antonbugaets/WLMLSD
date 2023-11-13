import logging
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_src.core.hashing import Hasher
from api_src.db.models import User

logger = logging.getLogger("UserDAL")


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        email: str,
        hashed_password: str,
        name: str,
    ) -> User:
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
        )

        self.db_session.add(new_user)
        await self.db_session.flush()

        logger.info(f"{email} registered")

        return new_user

    async def get_user_by_id(self, user_id) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()

        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()

        if user_row is not None:
            return user_row[0]

        return None

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)

        if not user:
            return False
        if not Hasher.verify_password(password, user.hashed_password):
            return False

        logger.info(f"{email} authenticated")

        return user
