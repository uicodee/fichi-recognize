from fastapi import FastAPI
from .recognize import router as recognize_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=recognize_router,
        tags=["Recognize"]
    )
