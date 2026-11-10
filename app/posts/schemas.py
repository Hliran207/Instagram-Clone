from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import ConfigDict

from app.users.schemas import UserSummary


class PostCreate(BaseModel):
    image_url: HttpUrl = Field(max_length=2048)
    caption: str = Field(max_length=2200, default="")


class PostUpdate(BaseModel):
    caption: str | None = Field(max_length=2200, default=None)


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: UserSummary
    image_url: str
    caption: str
    created_at: datetime
