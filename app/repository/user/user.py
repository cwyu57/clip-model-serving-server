import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.model.generated import Users


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_id(self, user_id: uuid.UUID) -> Users | None:
        result = await self._session.execute(select(Users).where(Users.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Users | None:
        result = await self._session.execute(
            select(Users).where(Users.username == username)
        )
        return result.scalar_one_or_none()
