from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dto.request_model import UpdateUserInfoRequest
from app.dto.response_model import UserResponse
from app.service.auth_service import AuthService
from app.service.database_service import DatabaseService
from app.service.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(AuthService.get_current_user)]
)


def get_user_service(db: Session = Depends(DatabaseService.get_db)):
    return UserService(db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_info(current_user: dict = Depends(AuthService.get_current_user),
                        user_service: UserService = Depends(get_user_service)):
    # print(current_user.get("username"))
    return user_service.get_user_info(current_user.get("id"))


@router.put("/update", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user_info(user_update_request: UpdateUserInfoRequest,
                           current_user: dict = Depends(AuthService.get_current_user),
                           user_service: UserService = Depends(get_user_service)):
    return user_service.update_user_info(current_user.get("id"), user_update_request)
