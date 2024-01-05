from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, RootModel

from app.models.hubs import HubResponse


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: str
    telegram_photo: Optional[str] = None


class UserCurrent(User):
    hub_id: Optional[int] = None


class UserWithLikes(User):
    like: Optional[bool] = None
    likesYou: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    about: Optional[str] = None
    age: Optional[int] = None
    firstName: str
    lastName: Optional[str] = None
    photo: Optional[str] = None
    hub: Optional[HubResponse] = None
    nickname: str


class UserInDatabase(User):
    updated_at: datetime
    created_at: datetime


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    start_param: Optional[Union[str, int]] = None


class TelegramUserInfo(BaseModel):
    about: Optional[str] = None
    photo: Optional[str] = None


class UsersResponseItem(BaseModel):
    id: int
    about: Optional[str] = None
    age: Optional[int] = None
    firstName: str
    lastName: Optional[str] = None
    photo: Optional[str] = None
    nickname: str
    like: Optional[bool] = None
    likesYou: Optional[bool] = None


class UsersResponse(RootModel):
    root: List[UsersResponseItem]
