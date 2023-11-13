from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "working"}, status_code=status.HTTP_200_OK)
