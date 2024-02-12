from datetime import datetime

from pydantic import BaseModel, Field


class EventRegistrationRequest(BaseModel):
    event_id: int = Field(gt=0)
    status: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


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
    organiser_id: int = Field(gt=0)
