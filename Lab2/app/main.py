import time
from fastapi import FastAPI
from .repository.database import engine, Base
from .repository import models
from .controller import notification_controller

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(notification_controller.router, prefix='/notifications')