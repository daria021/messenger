from fastapi import Depends, HTTPException, Cookie, Response
from fastapi.routing import APIRouter

from config import config
from .dependencies.repositories import get_auth_repo
from .exceptions import TokenEmptyException, TokenNotFoundException, TokenInvalidException, \
    TokenExpiredException, UserNotFound
from .repository import AuthorizationRepo
from .tokens import create_tokens, check_token, refresh_tokens, Tokens
from ..dependencies.repositories import get_user_repo
from ..repository import UserRepo

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def update_tokens_in_cookies(response: Response, tokens: Tokens):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    response.set_cookie(key="access_token", value=tokens.access_token, expires=config.ACCESS_EXPIRE_DAYS * 24 * 60 * 60)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, expires=config.REFRESH_EXPIRE_DAYS * 24 * 60 * 60)


def jwt_cookie_wrapper(
        access_token: str = Cookie(default=""),
        refresh_token: str = Cookie(default=""),
):
    return Tokens(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/create")
async def create_tokens_route(
        employee_id: int,
        response: Response,
        repo: AuthorizationRepo = Depends(get_auth_repo),
        user_repo: UserRepo = Depends(get_user_repo),
):
    try:
        tokens = await create_tokens(
            repo,
            user_repo,
            employee_id,
        )
    except:
        raise UserNotFound

    update_tokens_in_cookies(response, tokens)

    return tokens


@router.post("/check")
async def check_tokens_route(
        tokens: Tokens = Depends(jwt_cookie_wrapper),
        repo: AuthorizationRepo = Depends(get_auth_repo),
        user_repo: UserRepo = Depends(get_user_repo)
):
    try:
        return await check_token(
            repo=repo,
            user_repo=user_repo,
            received_tokens=tokens
        )
    except TokenEmptyException:
        raise HTTPException(status_code=400, detail="Token is empty")
    except TokenNotFoundException:
        raise HTTPException(status_code=404, detail="Token not found")
    except TokenInvalidException:
        raise HTTPException(status_code=400, detail="Token is invalid")
    except TokenExpiredException:
        raise HTTPException(status_code=400, detail="Token is expired")


@router.post("/refresh")
async def refresh_tokens_route(
        response: Response,
        tokens: Tokens = Depends(jwt_cookie_wrapper),
        repo: AuthorizationRepo = Depends(get_auth_repo),
        user_repo: UserRepo = Depends(get_user_repo)
):
    try:
        tokens = await refresh_tokens(
            repo,
            user_repo,
            tokens
        )

        update_tokens_in_cookies(response, tokens)

        return tokens

    except TokenEmptyException:
        raise HTTPException(status_code=400, detail="Token is empty")
    except TokenNotFoundException:
        raise HTTPException(status_code=404, detail="Token not found")
    except TokenInvalidException:
        raise HTTPException(status_code=400, detail="Token is invalid")
    except TokenExpiredException:
        raise HTTPException(status_code=400, detail="Token is expired")

#  employee: EmployeeResponse = Depends(check_tokens_route),
