from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.dto.request_model import CreateUserRequest
from app.dto.response_model import TokenResponse, UserResponse
from app.service.auth_service import AuthService
from app.service.database_service import DatabaseService

router = APIRouter(prefix="/auth", tags=["auth"])
db_service = DatabaseService()


def get_auth_service(db: Session = Depends(DatabaseService.get_db)) -> AuthService:
    return AuthService(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse,
             response_model_exclude={"id", "password"})
async def create_user(
        create_user_request: CreateUserRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    user_model = auth_service.create_user(create_user_request)
    return user_model


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_service.create_access_token(user.username, user.id, user.role, timedelta(minutes=2000))
    return {"access_token": token, "token_type": "Bearer"}
