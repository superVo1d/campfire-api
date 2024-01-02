import datetime
import os
from typing import List, Union

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.matches import Matches
from app.models.user import User, TelegramUser

load_dotenv()


class MongoDB:
    """A MongoDB database management class."""

    def __init__(self, uri: str, database: str) -> None:
        """Initializes a MongoDB connection using AsyncIOMotorClient."""
        self.cluster: AsyncIOMotorClient = AsyncIOMotorClient(uri)
        self.db = self.cluster[database]

    async def close(self) -> None:
        """Closes the database connection."""
        self.cluster.close()

    async def all_users(self) -> List[User]:
        """Returns all users list.

        Returns:
            List[User]: Collection of User objects.
        """
        _users = await self.db.users.find().to_list(length=None)

        users: list[User] = []

        for user in _users:
            users.append(User(
                user_id=user['user_id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                username=user['username'],
                telegram_photo=user['telegram_photo']
            ))

        return users

    async def update_or_create_user(self, user: TelegramUser) -> User:
        """Creates a new user if not exists.

        Args:
            user (TelegramUser): The user data.

        Returns:
            User: The User object.
        """

        _user = User(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        ).model_dump()

        await self.db.users.update_one({"user_id": user.id}, {"$set": _user}, upsert=True)

        result = await self.db.users.find_one({"user_id": user.id})

        return User(**result)

    async def get_user(self, user_id: int) -> Union[User, None]:
        """Returns user by id.

        Args:
            user_id: The user telegram id.

        Returns:
            User: The User object.
        """

        result = await self.db.users.find_one({"user_id": user_id})

        if result is None:
            return None

        return User(**result)

    async def like(self, first_user_id: int, second_user_id: int) -> Union[bool, None]:
        """Saves user`s like.

         Args:
            first_user_id: The user id.
            second_user_id: The liked user id.

        Returns:
            bool: Is mutual.
        """
        await self.db.matches.insert_one(
            Matches(first_user_id=first_user_id, second_user_id=second_user_id,
                    created_at=datetime.datetime.now()).model_dump())

        mutual_like = await self.db.matches.find_one(
            {'$or': [{'first_user_id': second_user_id}, {'second_user_id': first_user_id}]})

        return bool(mutual_like)


database = MongoDB(uri=os.getenv('MONGODB_URI'), database=os.getenv('DATABASE_NAME'))
