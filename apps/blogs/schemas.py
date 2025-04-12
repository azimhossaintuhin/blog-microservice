from pydantic import BaseModel, Field
from fastapi import Form, File, UploadFile
from uuid import UUID

class BlogOut(BaseModel):
    id: UUID
    author: UUID
    image: str
    title: str
    slug: str
    content: str
    category_id: UUID
    is_published: bool
    read_count: int = Field(..., alias="read_count_value")  # 👈 map to annotation

    class Config:
        from_attributes = True
        validate_by_name = True

class BlogIn(BaseModel):
    image:UploadFile
    title:str
    content:str
    category_id:UUID
    is_publised:bool
    tags:str
    
    @classmethod
    def as_form(
        cls,
        title:str = Form(...),
        content:str = Form(...),
        image:UploadFile = File(...),
        category_id:UUID = Form(...),
        is_publised:bool = Form(...),
        tags:str = Form(...)
    ):
        return cls(
           
            title=title,
            content=content,
            image=image,
            category_id=category_id,
            is_publised=is_publised,
            tags=tags
        )

class CategoryIN(BaseModel):
    name:str
    image:UploadFile
    
    @classmethod
    def as_form(cls,
                name:str=Form(None),
                image:UploadFile=File(None)):
        return cls(
            name=name,
            image=image
        )
        
class CategoryOut(BaseModel):
    id:UUID
    name:str
    slug:str
    image:str

