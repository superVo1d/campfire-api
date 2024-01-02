from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.models.user import User, UserResponse

router = APIRouter()


@router.get("", response_model=UserResponse, response_description="Get current user")
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return UserResponse(
        id=user.user_id,
        about='',
        age=None,
        firstName=user.first_name,
        lastName=user.last_name,
        photo=user.telegram_photo,
        hub='Campfire',
        nickname=user.username
    )
