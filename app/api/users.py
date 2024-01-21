from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.database.database import database
from app.models.user import UsersResponse, UsersResponseItem, UserCurrent

router = APIRouter()


@router.get("", response_model=UsersResponse, response_description="Get all users except the current one")
async def get_users(_user: Annotated[UserCurrent, Depends(get_current_user)]):
    _users = await database.all_users(_user.user_id, _user.hub_id)

    users: UsersResponse = []

    for user in _users:
        if user.user_id == _user.user_id:
            continue

        users.append(UsersResponseItem(
            id=user.user_id,
            about=user.about,
            age=None,
            firstName=user.first_name,
            lastName=user.last_name,
            like=user.like,
            likesYou=user.likesYou,
            nickname=user.username,
            photo=f'api/static/images/{user.telegram_photo}.jpg' if user.telegram_photo else None,
            workingName=user.working_name
        ))

    return users
