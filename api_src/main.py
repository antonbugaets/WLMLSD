import logging

import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api_src.api.middlewares import add_middlewares
from api_src.api.routers import users_router, tasks_router, metrics_router

app = FastAPI(title="Story2Animation", version="1.0.0")

app.include_router(users_router, prefix="/users")
app.include_router(tasks_router, prefix="/tasks")
app.include_router(metrics_router, prefix="/metrics")

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

add_middlewares(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=({"detail": str(exc.errors()[0]["msg"])}),
    )


@app.on_event("startup")
async def startup():
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized.")


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
