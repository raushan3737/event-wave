from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models.models import User, Event
from app.routers.admin import check_admin_permissions
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["event"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def check_user_exist(db: db_dependency, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail=f"Invalid organiser id: {user_id}")
    return True


class CreateEventRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=255)
    date: datetime
    time: datetime
    location: str = Field(min_length=3, max_length=255)
    max_attendees: int = Field(lt=1000)
    organiser_id: int = Field(gt=0)


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


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_event(user: user_dependency, db: db_dependency, create_event_request: CreateEventRequest):
    check_admin_permissions(user)
    check_user_exist(db, create_event_request.organiser_id)
    create_event_model = Event(
        title=create_event_request.title,
        description=create_event_request.description,
        date=create_event_request.date,
        time=create_event_request.time,
        location=create_event_request.location,
        max_attendees=create_event_request.max_attendees,
        organizer_id=create_event_request.organiser_id

    )
    db.add(create_event_model)
    db.commit()


@router.get("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponse,
            response_model_exclude={"max_attendees"})
async def get_event_info_by_id(user: user_dependency, db: db_dependency, event_id: int = Path(gt=0)):
    event_model = db.query(Event).filter(Event.id == event_id).first()
    if event_model is None:
        raise HTTPException(status_code=401, detail=f"Invalid event id: {event_id}")
    return jsonable_encoder(event_model)
