import datetime
from logging import getLogger
from typing import Optional

import jwt
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from config import config
from exceptions import NotFoundException
from .repository import AuthorizationRepo
from api.repository import UserRepo
from api.models import User
from .exceptions import (
    TokenInvalidException,
    TokenExpiredException,
    TokenNotFoundException,
    TokenEmptyException, UserNotFound,
)
from .schemas import AuthorizationCreate, AuthorizationUpdate

logger = getLogger(__name__)


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


async def create_tokens(repo: AuthorizationRepo,
                        user_repo: UserRepo,
                        employee_id: int,
                        received_tokens: Optional[Tokens] = None) -> Tokens:
    """
    Generate tokens for user
    :param session:
    :param employee_id:
    :param received_tokens: by default None
    :return: tokens dict
    {
        'access': str,
        'refresh': str,
    }
    """

    try:
        user = await check_token(received_tokens=received_tokens, repo=repo, user_repo=user_repo)
    except (TokenEmptyException, TokenNotFoundException):
        try:
            user = await user_repo.get(employee_id)
        except NotFoundException:
            raise UserNotFound

    except (TokenInvalidException, TokenExpiredException):
        user = await user_repo.get(employee_id)
        await repo.delete_by_user_id(user.id)

    tokens = AuthorizationCreate(
        access_token=jwt.encode(
            {
                'obj': user.id,
                'expires_on': (datetime.datetime.utcnow() +
                               datetime.timedelta(days=config.ACCESS_EXPIRE_DAYS)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
            key=config.JWT_SECRET.get_secret_value(),
            algorithm="HS256",
        ),
        refresh_token=jwt.encode(
            {
                'obj': user.id,
                'expires_on': (datetime.datetime.utcnow() +
                               datetime.timedelta(days=config.REFRESH_EXPIRE_DAYS)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
            key=config.JWT_SECRET.get_secret_value(),
            algorithm="HS256",
        ),
        user_id=user.id
    )

    try:
        auth = await repo.get_by_employee_id(employee_id)
        auth_id = auth.id
        await repo.delete(auth_id)
    except TokenNotFoundException:
        ...

    tokens = await repo.create(
        schema=tokens,
    )

    return tokens


async def refresh_tokens(repo: AuthorizationRepo,
                         user_repo: UserRepo,
                         received_tokens: Tokens = None) -> Tokens:
    """
    Refresh tokens
    :param session:
    :param received_tokens: tokens
    :return: new tokens
    """
    if not received_tokens:
        raise TokenEmptyException

    exist_token = await repo.get_by_refresh_token(
        received_tokens.refresh_token
    )

    if not exist_token:
        raise TokenNotFoundException

    try:
        refresh = jwt.decode(received_tokens.refresh_token,
                             key=config.JWT_SECRET.get_secret_value(),
                             algorithms="HS256",
                             verify=False)
    except jwt.exceptions.PyJWTError as e:
        logger.error(f'Invalid token: {e}')
        raise TokenInvalidException

    if datetime.datetime.strptime(refresh['expires_on'], '%Y-%m-%d %H:%M:%S.%f') < datetime.datetime.utcnow():
        raise TokenExpiredException

    user = await user_repo.get(refresh['obj'])

    tokens = {
        'access': jwt.encode(
            {
                'obj': user.id,
                'expires_on': (datetime.datetime.utcnow() +
                               datetime.timedelta(days=config.ACCESS_EXPIRE_DAYS)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
            key=config.JWT_SECRET.get_secret_value(),
            algorithm="HS256",
        ),
        'refresh': jwt.encode(
            {
                'obj': user.id,
                'expires_on': (datetime.datetime.utcnow() +
                               datetime.timedelta(days=config.REFRESH_EXPIRE_DAYS)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
            key=config.JWT_SECRET.get_secret_value(),
            algorithm="HS256",
        ),
    }

    schema = AuthorizationUpdate(
        access_token=tokens['access'],
        refresh_token=tokens['refresh']
    )
    tokens = await repo.update(
        exist_token.id,
        schema
    )

    return tokens


async def check_token(repo: AuthorizationRepo,
                      user_repo: UserRepo,
                      received_tokens: Optional[Tokens] = None) -> User:
    """
    Check token
    :param session:
    :param received_tokens: tokens
    :return: user
    """
    if not received_tokens:
        raise TokenEmptyException('No token provided')

    try:
        access = jwt.decode(received_tokens.access_token, config.JWT_SECRET.get_secret_value(), algorithms="HS256",
                            verify=False)
        refresh = jwt.decode(received_tokens.refresh_token, config.JWT_SECRET.get_secret_value(), algorithms="HS256",
                             verify=False)
    except jwt.exceptions.PyJWTError as e:
        logger.error(f'Invalid token: {e}')
        raise TokenInvalidException('Invalid token')

    user = await user_repo.get(access['obj'])
    try:
        exist_token = await repo.get_by_employee_id(user.id)
    except:
        raise TokenNotFoundException

    try:
        exist_access = jwt.decode(exist_token.access_token, config.JWT_SECRET.get_secret_value(), algorithms="HS256",
                                  verify=False)
        exist_refresh = jwt.decode(exist_token.refresh_token, config.JWT_SECRET.get_secret_value(), algorithms="HS256",
                                   verify=False)
    except jwt.exceptions.PyJWTError as e:
        logger.error(f'Invalid token: {e}')
        raise TokenInvalidException('Invalid token')

    if access['obj'] != refresh['obj']:
        logger.error('Invalid token: obj mismatch in received tokens')
        raise TokenInvalidException('Invalid token')
    if access != exist_access:
        logger.error('Invalid token: access token mismatch')
    if refresh != exist_refresh:
        logger.error('Invalid token: refresh token mismatch')

    if datetime.datetime.strptime(access['expires_on'], '%Y-%m-%d %H:%M:%S.%f') \
            < datetime.datetime.strptime(exist_access['expires_on'], '%Y-%m-%d %H:%M:%S.%f'
                                         ):
        raise TokenExpiredException('Access token expired')

    if datetime.datetime.strptime(refresh['expires_on'], '%Y-%m-%d %H:%M:%S.%f') \
            < datetime.datetime.strptime(exist_refresh['expires_on'], '%Y-%m-%d %H:%M:%S.%f'
                                         ):
        raise TokenExpiredException('Refresh token expired')

    return user
