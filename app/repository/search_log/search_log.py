from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.model.generated import SearchLogs


class SearchLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_search_log(self, query: str, image_url: str) -> SearchLogs:
        result = await self.session.execute(
            insert(SearchLogs)
            .values(query=query, image_url=image_url)
            .returning(SearchLogs)
        )
        return result.scalar_one()
