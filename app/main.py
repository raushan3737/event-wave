from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import engine, Base
from .exceptions.global_exception_handler import generic_exception_handler, database_exception_handler, \
    validation_exception_handler
from .router import auth_router, admin_router, user_router, event_router, attendee_router

app = FastAPI()

# will run only once, if the database does not exist.
Base.metadata.create_all(bind=engine)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log information about the incoming request
        print(f"Received request: {request.method} {request.url}")

        # Call the next middleware or route handler in the chain
        response = await call_next(request)

        # Log information about the outgoing response
        print(f"Sent response: {response.status_code}")

        return response


app.add_middleware(LoggingMiddleware)

# Adding routers:
app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(user_router.router)
app.include_router(event_router.router)
app.include_router(attendee_router.router)

# Adding global exception handlers:
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
