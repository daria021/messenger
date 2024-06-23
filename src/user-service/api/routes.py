from fastapi import APIRouter, Depends

from .dependencies.repositories import get_user_repo
from .repository import UserRepo
from .schemas import UserResponse, UserCreate, UserUpdate, UserFilter
from .models import User

router = APIRouter(
    prefix="/user",
    tags=["user/"]
)


@router.post("", response_model=UserResponse)
async def create_user(user: UserCreate,
                      users: UserRepo = Depends(get_user_repo)):
    user = await users.create(schema=user)
    return user

@router.get("/filter", response_model=list[UserResponse])
async def get_filter_users(filters: UserFilter = Depends(),
                           users: UserRepo = Depends(get_user_repo)
                           ) -> User:
    clean_filters = {key: value for key, value in filters.model_dump().items() if value is not None}
    res = await users.get_filtered_by(**clean_filters)
    return res


@router.get("/{user_id}", response_model=UserResponse)
async def get_one_user(user_id: int, users: UserRepo = Depends(get_user_repo)):
    res = await users.get(record_id=user_id)
    return res



@router.get("", response_model=list[UserResponse])
async def get_all_users(users: UserRepo = Depends(get_user_repo)
                        ) -> list[User]:
    res = await users.get_all()
    return res


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int,
                      update: UserUpdate,
                      users: UserRepo = Depends(get_user_repo)):
    user = await users.update(record_id=user_id, schema=update)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int,
                      users: UserRepo = Depends(get_user_repo)) -> None:
    await users.delete(record_id=user_id)
    return
