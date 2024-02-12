from datetime import datetime

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class EventRegistrationResponse(BaseModel):
    event_id: int
    user_id: int
    status: str
    registration_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EventResponse(BaseModel):
    title: str
    description: str
    date: str
    time: str
    location: str
    max_attendees: int
    organizer_id: int

    @classmethod
    def from_orm(cls, obj):
        obj.time = obj.time.strftime("%H:%M:%S") if obj.time else None
        return super().from_orm(obj)

    class Config:
        orm_mode = True
