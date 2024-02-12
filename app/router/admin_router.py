from typing import List

from fastapi import Depends, Path, APIRouter, status
from sqlalchemy.orm import Session

from app.dto.response_model import UserResponse, EventResponse
from app.service.admin_service import AdminService
from app.service.auth_service import AuthService
from app.service.database_service import DatabaseService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(AuthService.get_current_user_with_permissions)]
)

db_service = DatabaseService()


def get_admin_service(db: Session = Depends(DatabaseService.get_db)) -> AdminService:
    return AdminService(db)


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(admin_service: AdminService = Depends(get_admin_service)):
    return admin_service.get_all_users()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_user_by_id(
        user_id: int = Path(..., gt=0),
        admin_service: AdminService = Depends(get_admin_service)
):
    admin_service.delete_user_by_id(user_id)


@router.get("/events", status_code=status.HTTP_200_OK, response_model=List[EventResponse])
async def get_all_events(admin_service: AdminService = Depends(get_admin_service)):
    return admin_service.get_all_events()


@router.get("/attendees", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_attendees(admin_service: AdminService = Depends(get_admin_service)):
    return admin_service.get_all_attendees()
