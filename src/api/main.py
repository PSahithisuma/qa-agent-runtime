from fastapi import FastAPI

from src.db.database import (
    Base,
    engine
)

from src.api.routes.test_routes import (
    router as test_router
)

from src.api.routes.history_routes import (
    router as history_router
)

from src.api.routes.auth_routes import (
    router as auth_router
)

from src.api.routes.ws_routes import (
    router as ws_router
)

from src.api.routes.vector_routes import (
    router as vector_router
)

from src.api.routes.patch_routes import (
    router as patch_router
)
from prometheus_fastapi_instrumentator import (
    Instrumentator
)

from src.models import *


app = FastAPI(

    title="Autonomous QA Agent API",

    version="1.0.0"
)

Base.metadata.create_all(
    bind=engine
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    test_router,
    prefix="/api/v1/tests",
    tags=["Tests"]
)

app.include_router(
    history_router,
    prefix="/api/v1/history",
    tags=["History"]
)

app.include_router(
    vector_router,
    prefix="/api/v1/vector",
    tags=["Vector Memory"]
)

app.include_router(
    patch_router,
    prefix="/api/v1/patch",
    tags=["AI Patch Generation"]
)

app.include_router(
    ws_router
)


@app.get("/")
async def root():

    return {

        "message": (
            "QA Agent API Running"
        )
    }
Instrumentator().instrument(
    app
).expose(app)