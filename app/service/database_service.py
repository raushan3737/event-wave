from app.database import SessionLocal


class DatabaseService:
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
