import os

from celery import signature
from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, FileResponse

from api_src.api.pydantic_models import StatusResponse

router = APIRouter()


@router.post("/push")
async def push_task(text: str):
    task_id = signature('text2video', args=text).delay()

    return {'task_id': task_id.__str__()}


@router.get("/status")
async def get_status(task_id: str):
    task = AsyncResult(task_id)
    if task.ready() and task.status != 'REVOKED':
        path = task.get()

        return JSONResponse(
            content=StatusResponse(task_id=str(task), status=task.status, state=task.state, result=str(path)).dict(),
            status_code=status.HTTP_200_OK
        )

    else:
        return JSONResponse(
            content=StatusResponse(task_id=str(task), status=task.status, state=task.state, result="").dict(),
            status_code=status.HTTP_200_OK
        )


@router.delete("/cancel_task")
async def cancel_task(task_id: str):
    pass


@router.get("/download")
async def download(file_path: str):
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{file_path} not found')

    return FileResponse(file_path)
