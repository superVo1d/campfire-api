from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = ""
    username: str
    telegram_photo: Optional[str] = None


class UserInDatabase(User):
    updated_at: str
    created_at: str


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
