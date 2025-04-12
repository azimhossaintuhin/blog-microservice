import httpx
from fastapi import Request, HTTPException

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    token = token.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Token is invalid")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://users-app:3000/user",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
