from fastapi import HTTPException,status,Path
import httpx
from uuid import UUID

BLOG_BASE_URL = 'http://blogs-app:3000'
async def blog_exists(blog_id:UUID=Path(...)):
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog ID is required")
    try:
        if not isinstance(blog_id, UUID):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Blog ID format")
        async with  httpx.AsyncClient() as client:
            response = await client.get(
                f"{BLOG_BASE_URL}/blogs/{blog_id}",
            )
            print(response.json())
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Blog not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    