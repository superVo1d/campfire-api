from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HubXUser(BaseModel):
    hub_id: int
    user_id: int
    profile_id: Optional[int] = None
    created_at: datetime
