from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/images/{filename}")
def serve_static_files(filename: str):
    return FileResponse(f"./../f/images/{filename}")
