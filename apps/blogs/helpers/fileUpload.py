import os
import aiofiles
from fastapi import UploadFile, HTTPException, status

UPLOAD_DIRECTORY = "uploads"

os.mkdir(UPLOAD_DIRECTORY) if not os.path.exists(UPLOAD_DIRECTORY) else None

async def upload_images(file: UploadFile, fileaname: str ,destination:str) -> str:
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PNG, JPG, and JPEG are allowed."
        )
    image_extension = file.filename.split('.')[-1]
    fileaname = f"{fileaname}.{image_extension}"
    
    if not os.path.exists(os.path.join(UPLOAD_DIRECTORY,destination)):
        os.mkdir(os.path.join(UPLOAD_DIRECTORY,destination))
        
    destination = os.path.join(UPLOAD_DIRECTORY,destination)
    file_path = os.path.join(destination, fileaname)

    if os.path.exists(file_path):
        os.remove(file_path)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return file_path
