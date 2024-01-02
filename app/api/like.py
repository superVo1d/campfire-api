from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.database.database import database
from app.models.like import LikeResponse
from app.models.user import User

router = APIRouter()


@router.post("", response_model=LikeResponse, response_description="Like user")
async def like(id: int, user: Annotated[User, Depends(get_current_user)]):
    is_mutual = await database.like(user.user_id, id)

    return LikeResponse(mutual=is_mutual)
