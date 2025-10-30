from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.model.generated import SearchLogs
from app.entity.repository.search_log import CreateSearchLogInputSchema


class SearchLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_search_log(
        self, input_schema: CreateSearchLogInputSchema
    ) -> SearchLogs:
        result = await self.session.execute(
            insert(SearchLogs)
            .values(
                query=input_schema.query,
                image_url=input_schema.image_url,
                user_id=input_schema.user_id,
            )
            .returning(SearchLogs)
        )
        return result.scalar_one()
