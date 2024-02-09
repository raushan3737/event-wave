from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models.models import Attendee, Event
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/attendees",
    tags=["attendee"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class EventRegistrationRequest(BaseModel):
    event_id: int = Field(gt=0)
    status: str


class EventRegistrationResponse(BaseModel):
    event_id: int
    user_id: int
    status: str
    registration_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


@router.post("/registration", status_code=status.HTTP_200_OK, response_model=EventRegistrationResponse,
             response_model_exclude={"user_id", "event_id"})
async def register_event_by_id(user: user_dependency, db: db_dependency, event_registration: EventRegistrationRequest):
    event_model = db.query(Event).filter(Event.id == event_registration.event_id).first()

    if event_model is None or user is None:
        raise HTTPException(status_code=401, detail=f"Invalid event id: {event_registration.event_id}")

    user_id = user.get("id")
    attendee_model = Attendee(
        event_id=event_registration.event_id,
        user_id=user_id,
        status=event_registration.status,
    )
    db.add(attendee_model)
    db.commit()
    db.refresh(attendee_model)  # Refresh the model to get updated values
    return attendee_model
