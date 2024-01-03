from datetime import datetime

from pydantic import BaseModel


class Hub(BaseModel):
    hub_id: int
    hub_nm: str


class HubInDatabase(Hub):
    owner_user_id: int
    created_at: datetime
    updated_at: datetime


class HubResponse(BaseModel):
    hubId: int
    hubName: str
