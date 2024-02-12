from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class EventRegistrationRequest(BaseModel):
    event_id: int = Field(gt=0)
    status: str


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)
    role: str


class UpdateUserInfoRequest(BaseModel):
    email: Optional[str] = EmailStr
    first_name: Optional[str] = Field(min_length=3, max_length=100)
    last_name: Optional[str] = Field(min_length=3, max_length=100)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateEventRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=255)
    date: datetime
    time: datetime
    location: str = Field(min_length=3, max_length=255)
    max_attendees: int = Field(lt=1000)
