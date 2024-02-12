from fastapi import status

from app.dto.request_model import CreateEventRequest
from app.models.models import Event
from app.service.base_service import BaseService


class EventService(BaseService):
    def add_event(self, organizer_id: int, event_info: CreateEventRequest) -> Event:
        try:
            event_model = Event(**event_info.dict(), organizer_id=organizer_id)
            self.db.add(event_model)
            self.db.commit()
            return event_model
        except Exception as e:
            self.db.rollback()
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def get_event_info(self, event_id: int) -> Event:
        try:
            event_model = self.db.query(Event).filter(Event.id == event_id).first()
            if event_model is None:
                self.handle_exception(status.HTTP_404_NOT_FOUND, f"Event not found with id: {event_id}")

            return event_model
        except Exception as e:
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
