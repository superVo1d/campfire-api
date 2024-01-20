import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/images/{filename}")
def serve_static_files(filename: str):
    path = f"./../f/images/{filename}"

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Item not found")

    return FileResponse(path)
