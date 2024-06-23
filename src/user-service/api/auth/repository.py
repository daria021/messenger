from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from AbstractRepository import AbstractRepo
from .exceptions import TokenNotFoundException
from .models import Authorization
from .schemas import AuthorizationCreate, AuthorizationUpdate, AuthorizationResponse


class AuthorizationRepo(AbstractRepo):
    model = Authorization
    update_schema = AuthorizationUpdate
    create_schema = AuthorizationCreate
    get_schema = AuthorizationResponse

    async def get_by_refresh_token(self, refresh_token) -> AuthorizationResponse:
        try:
            res = await self.session.execute(
               select(self.model).where(self.model.refresh_token == refresh_token)
            )
            inst = res.scalar_one()
        except NoResultFound:
            raise TokenNotFoundException
        return self.get_schema.model_validate(inst)

    async def get_by_employee_id(self, user_id) -> AuthorizationResponse:
        try:
            res = await self.session.execute(
                select(self.model).where(self.model.user_id == user_id)
            )
            inst = res.scalar_one()
        except NoResultFound:
            raise TokenNotFoundException
        return self.get_schema.model_validate(inst)

    async def get_by_access_token(self, access_token) -> AuthorizationResponse:
        try:
            res = await self.session.execute(
                select(self.model).where(self.model.access_token == access_token)
            )
            inst = res.scalar_one()
        except NoResultFound:
            raise TokenNotFoundException
        return AuthorizationResponse.model_validate(inst) if inst else None

    async def delete_by_user_id(self, user_id):
        await self.session.execute(
            delete(self.model).where(self.model.user_id == user_id)
        )
        await self.session.commit()
