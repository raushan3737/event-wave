from fastapi import FastAPI

from app.database import engine, Base
from app.routers import auth, admin, user

app = FastAPI()

# will run only once, if the database does not exist.
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
