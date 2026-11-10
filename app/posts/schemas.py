from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, UrlConstraints

from app.users.schemas import UserSummary


class PostCreate(BaseModel):
    image_url: Annotated[HttpUrl, UrlConstraints(max_length=2048)]
    caption: str = Field(max_length=2200, default="")


class PostUpdate(BaseModel):
    caption: str = Field(max_length=2200)


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: UserSummary
    image_url: str
    caption: str
    created_at: datetime
