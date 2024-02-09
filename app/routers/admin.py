from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from app.database import SessionLocal

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
