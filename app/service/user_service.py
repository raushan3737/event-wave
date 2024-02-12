from starlette import status

from app.dto.request_model import UpdateUserInfoRequest
from app.models.models import User
from app.service.base_service import BaseService


class UserService(BaseService):

    def get_user_info(self, user_id: int):
        try:
            user_model = self.db.query(User).filter(User.id == user_id).first()
            return user_model
        except Exception as e:
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def update_user_info(self, user_id: int, update_request: UpdateUserInfoRequest):
        try:
            user_model = self.get_user_info(user_id)
            if not user_model:
                self.handle_exception(status.HTTP_404_NOT_FOUND, f"User not found with id : {user_id}")

            for field, value in update_request.dict(exclude_unset=True).items():
                setattr(user_model, field, value)

            self.db.commit()

            return user_model
        except Exception as e:
            self.db.rollback()
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
