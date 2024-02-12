from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status


class BaseService:
    def __init__(self, db: Session):
        self.db = db

    def handle_exception(self, code: status, error_message: str):
        raise HTTPException(status_code=code, detail=error_message)
