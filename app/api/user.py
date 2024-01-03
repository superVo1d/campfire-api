from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.bot.bot import bot
from app.database.database import database
from app.models.hubs import HubResponse
from app.models.user import UserCurrent, UserResponse

router = APIRouter()


@router.get("", response_model=UserResponse, response_description="Get current user")
async def get_user(user: Annotated[UserCurrent, Depends(get_current_user)]):
    hub = await database.get_user_hub(user.user_id, user.hub_id)

    telegram_user_info = await bot.load_user_info(user.user_id)

    return UserResponse(
        id=user.user_id,
        about=telegram_user_info.about,
        age=None,
        firstName=user.first_name,
        lastName=user.last_name,
        photo=user.telegram_photo,
        hub=HubResponse(hubId=hub.hub_id, hubName=hub.hub_nm),
        nickname=user.username
    )
