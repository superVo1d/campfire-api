from datetime import datetime

from pydantic import BaseModel


class Matches(BaseModel):
    first_user_id: int
    second_user_id: int
    created_at: datetime
