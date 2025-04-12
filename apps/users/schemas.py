from pydantic import BaseModel,Field ,EmailStr
from uuid import UUID
from fastapi import Form ,File ,UploadFile
import datetime
class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

    
class LoginUser(BaseModel):
    username: str = Field(None, min_length=3, max_length=50 )
    email: EmailStr = Field(None)
    password: str = Field(..., min_length=6, max_length=100)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    


class UserProfileIn(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    phone: str | None = None
    address: str | None = None
    profile_picture: UploadFile  # just type hint here

    @classmethod
    def as_form(
        cls,
        user_id: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone: str = Form(None),
        address: str = Form(None),
        profile_picture: UploadFile = File(...)
    ):
        return cls(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            profile_picture=profile_picture
        )


class UserProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    phone: str | None = None
    address: str | None = None
    profile_picture: str | None = None
    created_at: datetime.datetime
    