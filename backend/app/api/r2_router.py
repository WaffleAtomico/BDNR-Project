from typing import List, Optional

from app.lib.con_r2 import r2_conn
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/r2", tags=["R2"])

@router.post("/upload")
@r2_conn.validate_connection
async def upload_image_endpoint(file: UploadFile = File(...), folder: str = "images"):
    result = await r2_conn.upload_image(file, folder)
    return {
        "success": True,
        "message": "Image uploaded successfully",
        "data": result
    }