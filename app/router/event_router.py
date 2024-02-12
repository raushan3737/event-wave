from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from app.dto.request_model import CreateEventRequest
from app.dto.response_model import EventResponse
from app.service.auth_service import AuthService
from app.service.database_service import DatabaseService
from app.service.event_service import EventService

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(AuthService.get_current_user_with_permissions)]
)


def get_event_service(db: Session = Depends(DatabaseService.get_db)):
    return EventService(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def add_event(add_event_request: CreateEventRequest,
                    current_user: dict = Depends(AuthService.get_current_user_with_permissions),
                    event_service: EventService = Depends(get_event_service)):
    return event_service.add_event(current_user.get("id"), add_event_request)


@router.get("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponse)
async def get_event_info(event_id: int = Path(gt=0), event_service: EventService = Depends(get_event_service)):
    return event_service.get_event_info(event_id)
