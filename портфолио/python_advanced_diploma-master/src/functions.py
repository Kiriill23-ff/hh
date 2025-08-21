from pathlib import Path

import aiofiles
from fastapi import UploadFile
from werkzeug.utils import secure_filename

from src.handlers.exceptions import FileException


async def allowed_file(filename: str) -> bool:
    allowed_extensions = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

    return "." in filename and filename.rsplit(".", 1)[1] in allowed_extensions


async def save_uploaded_file(api_key: str, upload_file: UploadFile) -> str:
    upload_folder = Path(__file__).parent.parent / "media" / secure_filename(api_key)
    upload_folder.mkdir(parents=True, exist_ok=True)

    if upload_file.filename is None or not await allowed_file(upload_file.filename):
        raise FileException("File format is not allowed. Please upload a valid file.")

    filename = upload_file.filename
    filename = secure_filename(filename)
    output_file = (upload_folder / filename).resolve()

    if not str(output_file).startswith(str(upload_folder)):
        raise FileException("Attempt to write outside the media directory.")

    async with aiofiles.open(output_file, "wb") as opened_file:
        await opened_file.write(await upload_file.read())

    return str(output_file)
