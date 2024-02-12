from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import User, Event, Attendee


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def check_admin_permissions(self, user: dict):
        if user is None or user.get("user_role") != "Admin":
            raise HTTPException(status_code=401, detail="You don't have permission of admin")

    def get_all_users(self):
        return self.db.query(User).all()

    def delete_user_by_id(self, user_id: int):
        user_model = self.db.query(User).filter(User.id == user_id).first()
        if not user_model:
            raise HTTPException(status_code=404, detail=f"User not found with id: {user_id}")

        self.db.delete(user_model)
        self.db.commit()

    def get_all_events(self):
        return self.db.query(Event).all()

    def get_all_attendees(self):
        return self.db.query(Attendee).all()
