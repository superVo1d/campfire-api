import os

from aiogram import Bot
from dotenv import load_dotenv

from app.models.user import TelegramUserInfo

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


class TelegramBot:
    """A Telegram bot class."""

    def __init__(self, token: str, parse_mode: str = "html") -> None:
        """Initializes a MongoDB connection using AsyncIOMotorClient."""
        self.bot = Bot(token=token, parse_mode=parse_mode)

    async def load_user_info(self, user_id: str) -> TelegramUserInfo:
        """Load telegram user's info.

        Args:
            user (TelegramUser): The user data.
        """

        user = await self.bot.get_chat(user_id)

        return TelegramUserInfo(about=user.bio, photo=None)


bot = TelegramBot(token=BOT_TOKEN, parse_mode='html')
