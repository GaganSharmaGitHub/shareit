from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from fastapi.responses import FileResponse
from datetime import datetime
from models.file_model import FileModel
from utils.auth_decorator import auth_required
from utils.db_utils import DBUtils
import os
from uuid import uuid4

router = APIRouter()

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/files/upload", response_model=FileModel)
@auth_required
def upload_file(request: Request, file: UploadFile = File(...)):
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, file_id + "_" + file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    file_metadata = FileModel(
        id=file_id,
        file_path=file_path,
        uploaded_at=datetime.now(),
        user_id=request.state.user.id,
        file_name=file.filename,
    )
    DBUtils.create(file_metadata)
    return file_metadata


@router.get("/files", response_model=list[FileModel])
@auth_required
def list_files(request: Request):
    return DBUtils.find(FileModel, {"user_id": request.state.user.id})


@router.get("/files/download/{file_id}")
@auth_required
def download_file(request: Request, file_id: str):
    files = DBUtils.find(FileModel, {"id": file_id, "user_id": request.state.user.id})
    if not files:
        raise HTTPException(status_code=404, detail="File not found")
    file_metadata = files[0]
    return FileResponse(
        file_metadata.file_path,
        media_type="application/octet-stream",
        filename=os.path.basename(file_metadata.file_path),
    )
