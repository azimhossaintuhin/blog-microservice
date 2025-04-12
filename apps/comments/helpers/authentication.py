import httpx 
from  fastapi import   HTTPException,Request
USER_BSAE_URL = 'http://users-app:3000/user'



async def get_current_user(request:Request):
    token = request.headers.get("Authorization")
    
    if not token:
        return HTTPException(status_code=401, detail="Token is missing")
    token = token.split(" ")[1]
    if not token:
        return HTTPException(status_code=401, detail="Token is invalid")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                USER_BSAE_URL,
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
