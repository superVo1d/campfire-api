import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from telegram_webapp_auth import parse_user_data, parse_init_data, validate

from app.models.user import TelegramUser

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


def verify_token(auth_cred: HTTPAuthorizationCredentials) -> TelegramUser:
    init_data = auth_cred.credentials

    try:
        if validate(init_data, BOT_TOKEN):
            raise ValueError("Invalid hash")
    except ValueError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    init_data = parse_init_data(init_data)
    user_data = parse_user_data(init_data["user"])

    start_param = None

    try:
        start_param = int(init_data.get("start_param"))
    except:
        pass

    return TelegramUser(start_param=start_param, **user_data)


telegram_authentication_schema = HTTPBearer()


def get_telegram_user(
        auth_cred: Annotated[HTTPAuthorizationCredentials, Depends(telegram_authentication_schema)]
) -> TelegramUser:
    return verify_token(auth_cred)
