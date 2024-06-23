from AbstractRepository import AbstractRepo
from .schemas import UserUpdate, UserCreate, UserResponse
from .models import User


class UserRepo(AbstractRepo):
    model = User
    update_schema = UserUpdate
    create_schema = UserCreate
    get_schema = UserResponse
