from starlette import status

from app.models.models import User, Event, Attendee
from app.service.base_service import BaseService


class AdminService(BaseService):
    # def check_admin_permissions(self, user: dict):
    #     try:
    #         if user is None or user.get("user_role") != "Admin":
    #             self.handle_exception(status.HTTP_403_FORBIDDEN, "You don't have permission of admin")
    #     except Exception as e:
    #         self.handle_exception(status.HTTP_401_UNAUTHORIZED, str(e))

    def get_all_users(self):
        try:
            return self.db.query(User).all()
        except Exception as e:
            self.handle_exception(status.HTTP_404_NOT_FOUND, str(e))

    def delete_user_by_id(self, user_id: int):
        try:
            user_model = self.db.query(User).filter(User.id == user_id).first()
            if not user_model:
                self.handle_exception(status.HTTP_404_NOT_FOUND, f"User not found with id: {user_id}")

            self.db.delete(user_model)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.handle_exception(status.HTTP_304_NOT_MODIFIED, str(e))

    def get_all_events(self):
        try:
            return self.db.query(Event).all()
        except Exception as e:
            self.handle_exception(status.HTTP_404_NOT_FOUND, str(e))

    def get_all_attendees(self):
        try:
            return self.db.query(Attendee).all()
        except Exception as e:
            self.handle_exception(status.HTTP_404_NOT_FOUND, str(e))
