from datetime import date, time

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str


class EventResponse(BaseModel):
    title: str
    description: str
    date: date
    time: time
    location: str
    max_attendees: int
    organizer_id: int


class AttendeeResponse(BaseModel):
    user_id: int
    event_id: int
    status: str
