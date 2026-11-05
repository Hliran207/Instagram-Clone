from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9._]+$")
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(max_length=30, default=None)
    bio: str | None = Field(max_length=150, default=None)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    full_name: str | None = Field(default=None)
    bio: str | None = Field(default=None)
    created_at: datetime
