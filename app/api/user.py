from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.bot.bot import bot
from app.database.database import database
from app.models.hubs import HubResponse
from app.models.user import UserCurrent, UserResponse, UserUpdate

router = APIRouter()


@router.get("", response_model=UserResponse, response_description="Get current user")
async def get_user(user: Annotated[UserCurrent, Depends(get_current_user)]):
    hub = await database.get_user_hub(user.user_id, user.hub_id)

    telegram_user_info = await bot.load_user_info(user.user_id)

    return UserResponse(
        id=user.user_id,
        about=user.about,
        age=user.age,
        firstName=user.first_name,
        lastName=user.last_name,
        workingName=user.working_name,
        photo=f'api/static/images/{telegram_user_info.photo}.jpg' if telegram_user_info.photo else None,
        hub=HubResponse(hubId=hub.hub_id, hubName=hub.hub_nm) if hub else None,
        nickname=user.username
    )


@router.patch("", response_description="Update user info")
async def update_user(user: Annotated[UserCurrent, Depends(get_current_user)], values: UserUpdate):
    _user = await database.update_user(user.user_id, values)

    hub = await database.get_user_hub(_user.user_id, user.hub_id)

    telegram_user_info = await bot.load_user_info(user.user_id)

    return UserResponse(
        id=_user.user_id,
        about=_user.about,
        age=_user.age,
        firstName=_user.first_name,
        lastName=_user.last_name,
        workingName=_user.working_name,
        photo=f'api/static/images/{telegram_user_info.photo}.jpg' if telegram_user_info.photo else None,
        hub=HubResponse(hubId=hub.hub_id, hubName=hub.hub_nm) if hub else None,
        nickname=_user.username
    )
