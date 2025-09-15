from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.employees import router as employees_router
from app.api.routes.time_records import router as time_records_router
from app.models.employee import Base
from app.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(employees_router)
    app.include_router(time_records_router)

    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    # Simple metadata creation without Alembic for first run
    Base.metadata.create_all(bind=engine)


