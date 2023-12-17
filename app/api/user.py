from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=User, response_description="Get current user")
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user
