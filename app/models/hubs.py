from datetime import datetime

from pydantic import BaseModel


class Hubs(BaseModel):
    hub_id: int
    hub_nm: str
    owner_user_id: int
    created_at: datetime
    updated_at: datetime
