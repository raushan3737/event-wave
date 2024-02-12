from starlette import status

from app.dto.request_model import EventRegistrationRequest
from app.models.models import Attendee
from app.service.base_service import BaseService
from app.service.event_service import EventService
from app.service.user_service import UserService


class AttendeeService(BaseService):
    def __init__(self, db, user_service: UserService, event_service: EventService):
        super().__init__(db)
        self.user_service = user_service
        self.event_service = event_service

    def register_event(self, user_id: int, event_request: EventRegistrationRequest) -> Attendee:
        try:
            user_model = self.user_service.get_user_info(user_id)
            event_model = self.event_service.get_event_info(event_request.event_id)

            existing_attendee = self.db.query(Attendee).filter(Attendee.user_id == user_id,
                                                               Attendee.event_id == event_request.event_id).first()
            if existing_attendee:
                self.handle_exception(status.HTTP_400_BAD_REQUEST, "User is already registered for the event")

            # Register the user for the event
            if event_model and user_model and not existing_attendee:
                attendee_model = Attendee(user_id=user_id, event_id=event_request.event_id, status=event_request.status)
                self.db.add(attendee_model)
                self.db.commit()
                return attendee_model

        except Exception as e:
            self.db.rollback()
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
