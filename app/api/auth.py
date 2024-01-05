import os
from datetime import timedelta, datetime
from typing import Union, Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.bot.bot import bot
from app.database.database import database
from app.models.token import TokenData, Token
from app.models.user import TelegramUser, UserCurrent, User
from app.utils.utils import get_telegram_user

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_user(user_id: int) -> Union[User, None]:
    return await database.get_user(user_id)


async def get_user_hub(user_id: int, hub_id: Union[int, str, None]) -> Union[int, None]:
    hub = await database.get_user_hub(user_id, hub_id)

    return hub.hub_id if hub else None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserCurrent:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        hub_id = payload.get("hub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, hub_id=hub_id)
    except JWTError:
        raise credentials_exception

    user = await get_user(token_data.user_id)
    hub_id = await get_user_hub(token_data.user_id, token_data.hub_id)

    if user is None:
        raise credentials_exception

    return UserCurrent(hub_id=hub_id, **user.model_dump())


@router.post("", response_model=Token, response_description="Authenticate user")
async def auth(telegram_user: TelegramUser = Depends(get_telegram_user)):
    telegram_user_info = await bot.load_user_info(telegram_user.id)

    user = await database.update_or_create_user(telegram_user, telegram_user_info)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "hub": telegram_user.start_param}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
