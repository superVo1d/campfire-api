import os
import urllib.request

from aiogram import Bot
from dotenv import load_dotenv

from app.models.user import TelegramUserInfo

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


class TelegramBot:
    """A Telegram bot class."""

    def __init__(self, token: str, parse_mode: str = "html") -> None:
        """Initializes a MongoDB connection using AsyncIOMotorClient."""
        self.token = token
        self.bot = Bot(token=self.token, parse_mode=parse_mode)

    async def load_user_info(self, user_id: str) -> TelegramUserInfo:
        """Loads telegram user's bio and photo. Downloads image.

        Args:
            user_id: Telegram user id.

        Returns:
            TelegramUserInfo: Telegram user info object.
        """

        user = await self.bot.get_chat(user_id)
        file_name = f'{user_id}.jpg'

        if user.photo:
            file_id = user.photo.big_file_id

            try:
                file = await self.bot.get_file(file_id)

                file_path = f'https://api.telegram.org/file/bot{self.token}/{file.file_path}'

                if not os.path.isfile(f"./../f/images/{file_name}"):
                    urllib.request.urlretrieve(file_path, f"./../f/images/{file_name}")
                    os.chmod(file_path, 0o777)
            except:
                pass

        return TelegramUserInfo(about=user.bio, photo=str(user_id) if file_name else None)


bot = TelegramBot(token=BOT_TOKEN, parse_mode='html')
