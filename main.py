from fastapi import FastAPI

from database.config import engine
from database.base import Base
from router import login
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=login.router, prefix='/api')
