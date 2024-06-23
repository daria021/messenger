from typing import Type

from AbstractRepository import AbstractRepo, Schema


class AbstractService:
    repo_type: Type[AbstractRepo] = AbstractRepo

    def __init__(self, repo: repo_type):
        self.repository = repo

    async def get(self, record_id: int) -> repo_type.get_schema:
        return await self.repository.get(record_id=record_id)

    async def get_all(self, *filters, offset: int = 0, limit: int = 100) -> list[repo_type.get_schema]:
        return await self.repository.get_all(*filters, offset=offset, limit=limit)

    async def create(self, schema: repo_type.create_schema) -> repo_type.get_schema:
        return await self.repository.create(schema=schema)

    async def update(self, record_id: int, schema: repo_type.update_schema) -> repo_type.get_schema:
        return await self.repository.update(record_id=record_id, schema=schema)

    async def delete(self, record_id: int) -> None:
        await self.repository.delete(record_id=record_id)

    async def get_filtered_by(self, **kwargs) -> list[Schema]:
        return await self.repository.get_filtered_by(**kwargs)
