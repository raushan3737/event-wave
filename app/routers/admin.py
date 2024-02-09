from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models.models import User, Event, Attendee
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def check_admin_permissions(user: dict):
    if user is None or user.get("user_role") != "Admin":
        raise HTTPException(status_code=401, detail="You don't have permission of admin")


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db: db_dependency):
    check_admin_permissions(user)
    return db.query(User).all()


@router.delete("/users/{users_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user: user_dependency, db: db_dependency, users_id: int = Path(..., gt=0)):
    check_admin_permissions(user)

    user_model = db.query(User).filter(User.id == users_id).first()
    if not user_model:
        raise HTTPException(status_code=404, detail=f"Todo is not found with id: {users_id}")

    db.delete(user_model)
    db.commit()


@router.get("/events", status_code=status.HTTP_200_OK)
async def get_all_events(user: user_dependency, db: db_dependency):
    check_admin_permissions(user)
    return db.query(Event).all()


@router.get("/attendees", status_code=status.HTTP_200_OK)
async def get_all_attendees(user: user_dependency, db: db_dependency):
    check_admin_permissions(user)
    return db.query(Attendee).all()
