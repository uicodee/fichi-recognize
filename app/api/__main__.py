import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import controllers
from app.config import load_config


def main() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        version="1.0.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    controllers.setup(app)
    return app


if __name__ == '__main__':
    uvicorn.run(
        "app.api.__main__:main",
        host="0.0.0.0",
        port=15400,
        reload=True
    )
