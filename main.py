from fastapi import FastAPI

import models
from database import engine
from routers.device_router import router as device_router
from routers.statistics_router import router as statistics_router
from routers.user_router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(device_router)
app.include_router(statistics_router)
app.include_router(user_router)


