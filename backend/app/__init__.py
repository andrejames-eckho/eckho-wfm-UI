# app/__init__.py
from fastapi import FastAPI
from .database import engine, Base
from . import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Import and include routers
from .routes import users, time_records
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(time_records.router, prefix="/time-records", tags=["time-records"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Eckho WFM API"}