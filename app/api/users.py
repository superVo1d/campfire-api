from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.database.database import database
from app.models.user import UsersResponse, UsersResponseItem, User

router = APIRouter()


@router.get("", response_model=UsersResponse, response_description="Get all users except the current one")
async def get_users(_user: Annotated[User, Depends(get_current_user)]):
    _users = await database.all_users()

    users: UsersResponse = []

    for user in _users:
        if user.user_id == _user.user_id:
            continue

        users.append(UsersResponseItem(
            id=user.user_id,
            about=None,
            age=None,
            firstName=user.first_name,
            lastName=user.last_name,
            photo=user.telegram_photo,
            nickname=user.username,
            match=None
        ))

    return users
