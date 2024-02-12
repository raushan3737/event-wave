from fastapi import FastAPI

from app.database import engine, Base
from .router import auth_router, admin_router

app = FastAPI()

# will run only once, if the database does not exist.
Base.metadata.create_all(bind=engine)

# Adding routers:
app.include_router(auth_router.router)
app.include_router(admin_router.router)
# app.include_router(user.router)
# app.include_router(event.router)
# app.include_router(attendee.router)

# Adding global exception handlers:
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(Exception, generic_exception_handler)
# app.add_exception_handler(SQLAlchemyError, database_exception_handler)
