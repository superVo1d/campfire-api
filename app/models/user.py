from datetime import datetime
from typing import Optional, Literal, List

from pydantic import BaseModel, RootModel


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: str
    telegram_photo: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    about: str
    age: Optional[int] = None
    firstName: str
    lastName: Optional[str] = None
    photo: Optional[str] = None
    hub: str
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


class UsersResponseItem(BaseModel):
    id: int
    about: Optional[str] = None
    age: Optional[int] = None
    firstName: str
    lastName: Optional[str] = None
    photo: Optional[str] = None
    nickname: str
    match: Optional[Literal['you', 'your', 'mutual']] = None


class UsersResponse(RootModel):
    root: List[UsersResponseItem]
