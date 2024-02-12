from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dto.request_model import EventRegistrationRequest
from app.dto.response_model import AttendeeResponse
from app.service.attendee_service import AttendeeService
from app.service.auth_service import AuthService
from app.service.database_service import DatabaseService
from app.service.event_service import EventService
from app.service.user_service import UserService

router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
    dependencies=[Depends(AuthService.get_current_user)]
)

db_service = DatabaseService()


def get_attendee_service(db: Session = Depends(db_service.get_db)) -> AttendeeService:
    user_service = UserService(db)
    event_service = EventService(db)
    return AttendeeService(db, user_service, event_service)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AttendeeResponse,
             response_model_exclude={"user_id"})
async def register_attendee(
        event_request: EventRegistrationRequest,
        current_user: dict = Depends(AuthService.get_current_user),
        attendee_service: AttendeeService = Depends(get_attendee_service),
):
    return attendee_service.register_event(current_user.get("id"), event_request)
