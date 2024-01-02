from datetime import datetime

from pydantic import BaseModel


class HubXUser(BaseModel):
    hub_id: int
    user_id: int
    profile_id: int
    created_at: datetime
