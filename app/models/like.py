from pydantic import BaseModel


class LikeResponse(BaseModel):
    mutual: bool
