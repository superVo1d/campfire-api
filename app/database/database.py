import datetime
import os
from typing import List, Union, Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.hub_x_user import HubXUser
from app.models.hubs import Hub
from app.models.matches import Matches
from app.models.user import User, TelegramUser, UserWithLikes, TelegramUserInfo

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

    async def all_users(self, user_id: int, hub_id: int) -> List[UserWithLikes]:
        """Returns all users list.

        Returns:
            List[User]: Collection of User objects.
        """

        users: list[UserWithLikes] = []

        pipeline = [
            {
                "$match": {"hub_id": hub_id}
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$match": {"user.user_id": {"$ne": user_id}}
            },
            {
                "$lookup": {
                    "from": "matches",
                    "localField": "user_id",
                    "foreignField": "second_user_id",
                    "as": "like",
                    "pipeline": [
                        {"$match": {"first_user_id": user_id}}
                    ]
                }
            },
            {
                "$lookup": {
                    "from": "matches",
                    "localField": "user_id",
                    "foreignField": "first_user_id",
                    "as": "likes_you",
                    "pipeline": [
                        {"$match": {"second_user_id": user_id}}
                    ]
                }
            }
        ]

        async for result in self.db.hub_x_user.aggregate(pipeline):
            print(result['like'])
            _user = result['user']
            like = result['like'][0] if result['like'] else None
            likes_you = result['likes_you'][0] if result['likes_you'] else None

            users.append(UserWithLikes(
                user_id=_user['user_id'],
                first_name=_user['first_name'],
                last_name=_user['last_name'],
                username=_user['username'],
                telegram_photo=_user['telegram_photo'],
                like=bool(like),
                likesYou=bool(likes_you)
            ))

        return users

    async def update_or_create_user(self, telegram_user: TelegramUser,
                                    telegram_user_info: TelegramUserInfo = None) -> User:
        """Creates a new user if not exists.

        Args:
            telegram_user (TelegramUser): The user data.

            telegram_user_info (TelegramUserInfo): Telegram bot additional userdata.

        Returns:
            User: The User object.
        """

        _user = User(
            user_id=telegram_user.id,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            username=telegram_user.username,
            telegram_photo=telegram_user_info.photo
        ).model_dump()

        await self.db.users.update_one(
            {
                "user_id": telegram_user.id
            },
            [{
                "$set": {
                    "updated_at": datetime.datetime.now(),
                    "created_at": {
                        "$cond": [
                            {"$ne": ['$created_at', None]},
                            datetime.datetime.now(),
                            "$created_at"
                        ]
                    },
                    "about": {
                        "$cond": [
                            {"$ne": ['$about', None]},
                            telegram_user_info.about,
                            "$about"
                        ]
                    },
                    **_user,
                }
            }], upsert=True)

        # await self.db.users.update_one(
        #     {
        #         "user_id": telegram_user.id
        #     },
        #     {
        #         "$setOnInsert": {
        #             "created_at": datetime.datetime.now(),
        #         },
        #         "$set": {
        #             "updated_at": datetime.datetime.now(),
        #             "telegram_photo": {
        #                 "$cond": [
        #                     {"$ne": [
        #                         "$telegram_photo",
        #                         None
        #                     ]},
        #                     telegram_user_info.photo,
        #                     "$telegram_photo"
        #                 ]
        #             },
        #             "about": {
        #                 "$cond": [
        #                     {"$ne": [
        #                         "$about",
        #                         None
        #                     ]},
        #                     telegram_user_info.about,
        #                     "$about"
        #                 ]
        #             },
        #             **_user
        #         }
        #     }, upsert=True)

        print('telegram_user.start_param', telegram_user.start_param)

        # Check if hub exists
        hub = await self.db.hubs.find_one(
            {"hub_id": int(telegram_user.start_param)}) if telegram_user.start_param else None

        if hub:
            hub_x_user = await self.db.hub_x_user.find_one(
                {"hub_id": int(telegram_user.start_param), "user_id": telegram_user.id})

            # If hub_x_user document doesn't exist create the one.
            if not hub_x_user:
                await self.db.hub_x_user.insert_one(
                    HubXUser(
                        hub_id=int(telegram_user.start_param),
                        user_id=telegram_user.id,
                        created_at=datetime.datetime.now()
                    ).model_dump())

        result = await self.db.users.find_one({"user_id": telegram_user.id})

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

    async def like(self, first_user_id: int, second_user_id: int) -> bool:
        """Toggles user`s like.

         Args:
            first_user_id: The user id.
            second_user_id: The liked user id.

        Returns:
            bool: Like is mutual.
        """

        like = await self.db.matches.find_one({'first_user_id': first_user_id, 'second_user_id': second_user_id})

        if like:
            await self.db.matches.delete_many({'first_user_id': first_user_id, 'second_user_id': second_user_id})
        else:
            await self.db.matches.insert_one(
                Matches(first_user_id=first_user_id, second_user_id=second_user_id,
                        created_at=datetime.datetime.now()).model_dump())

        mutual_like = await self.db.matches.find_one(
            {'$or': [{'first_user_id': second_user_id}, {'second_user_id': first_user_id}]})

        return bool(mutual_like)

    async def get_user_hub(self, user_id: int, hub_id: Optional[int] = None) -> Union[Hub, None]:
        """Returns hub related to user.

        Args:
            user_id: The user telegram id.

        Returns:
            Hub: The Hub object.
        """

        hub_x_user = await self.db.hub_x_user.find_one({"user_id": user_id, "hub_id": hub_id})

        if hub_x_user:
            _hub = await self.db.hubs.find_one({"hub_id": hub_x_user['hub_id']})

            return Hub(**_hub)
        else:
            hub_x_user = await self.db.hub_x_user.find_one({"user_id": user_id})

            if hub_x_user:
                _hub = await self.db.hubs.find_one({"hub_id": hub_x_user['hub_id']})

                return Hub(**_hub)

        return None


database = MongoDB(uri=os.getenv('MONGODB_URI'), database=os.getenv('DATABASE_NAME'))
