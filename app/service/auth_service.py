import logging
import os
from datetime import timedelta, datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from app.dto.request_model import CreateUserRequest
from app.models.models import User
from app.service.base_service import BaseService

load_dotenv()
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthService(BaseService):
    def create_user(self, create_user_request: CreateUserRequest):
        try:
            create_user_model = User(
                email=create_user_request.email,
                username=create_user_request.username,
                first_name=create_user_request.first_name,
                last_name=create_user_request.last_name,
                role=create_user_request.role,
                password=bcrypt_context.hash(create_user_request.password),
            )
            self.db.add(create_user_model)
            self.db.commit()
            return create_user_model
        except Exception as e:
            self.db.rollback()
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        try:
            user = self.db.query(User).filter(User.username == username).first()
            if not user or not bcrypt_context.verify(password, user.password):
                self.handle_exception(status.HTTP_401_UNAUTHORIZED, "Could not validate the user")
            return user
        except Exception as e:
            self.handle_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            user_role: str = payload.get("role")
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")
            return {"username": username, "id": user_id, "user_role": user_role}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")

    @staticmethod
    def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
        try:
            encode = {"sub": username, "id": user_id, "role": role}
            expires = datetime.utcnow() + expires_delta
            encode.update({"exp": expires})
            return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        except Exception as e:
            logger.error(f"An error occurred while creating an access token: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create access token")

    @staticmethod
    async def get_current_user_with_permissions(token: str = Depends(oauth2_bearer)) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            user_role: str = payload.get("role")
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")

            # Check admin permissions
            if user_role != "Admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission of admin")

            return {"username": username, "id": user_id, "user_role": user_role}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")
