from fastapi import FastAPI, HTTPException, status ,Depends
from tortoise import Tortoise
from config.Database import TORTOISE_ORM
from  contextlib import asynccontextmanager
from schemas import BlogOut,BlogIn ,CategoryIN,CategoryOut
from models import Blog , Category
from  helpers.authentication import verify_token
from helpers.fileUpload import UPLOAD_DIRECTORY, upload_images
from  tortoise.functions import Count

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()



app = FastAPI(
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Welcome to the blog user service"}


@app.get("/blogs", response_model=list[BlogOut] | dict[str, str])
async def get_blogs():
    blogs = await Blog.annotate(
        read_count_value=Count("read_count")  # 👈 use a different name
    ).prefetch_related("category").all()
    
    if not blogs:
        return {"message": "No blogs found"}

    return blogs

@app.post("/blogs/create", response_model=BlogOut)
async def create_blog(blog: BlogIn = Depends(BlogIn.as_form), current_user=Depends(verify_token)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    blog_obj = await Blog.create(
        title=blog.title,
        author=current_user.get("id"),
        content=blog.content,
        category=await Category.filter(id=blog.category_id).first(),
        tags=blog.tags,
        image=await upload_images(blog.image, blog.title.replace(" ", "-").lower(), "blogs"),
    )

    # Return the blog as a dict with read_count set to 0 initially
    return {
        "id": blog_obj.id,
        "author": blog_obj.author,
        "image": blog_obj.image,
        "title": blog_obj.title,
        "slug": blog_obj.slug,
        "content": blog_obj.content,
        "category_id": blog_obj.category_id,
        "is_published": blog_obj.is_published,
        "read_count": 0,  # New blogs have 0 read count
    }

@app.get("/category", response_model=list[CategoryOut]|dict[str, str])
async def all_category():
    category = await Category.all()
    
    return category

@app.post("/category/create/", response_model=CategoryOut)
async def  create_category(data:CategoryIN=Depends(CategoryIN.as_form)):
    category = await Category.create(
        name=data.name,
        image= await upload_images(data.image, data.name,destination="categories")
    )
    await category.save()
   
    return category

@app.patch("/category/update/{category_id}", response_model=dict[str, str])
async def category_update(
    category_id: str,
    data: CategoryIN = Depends(CategoryIN.as_form),
    current_user: dict = Depends(verify_token)
):
    category = await Category.filter(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if data.name:
        category.name = data.name
    if data.image:
        category.image = await upload_images(data.image, data.name, "categroy")

    await category.save()
    return {"message": "Category updated successfully"}


@app.put("/blogs/update/{blog_id}", response_model=BlogOut)
async def update_blog(
    blog_id: str,
    data: BlogIn = Depends(BlogIn.as_form),
    current_user: dict = Depends(verify_token)
):
    blog = await Blog.filter(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if data.title:
        blog.title = data.title
    if data.content:
        blog.content = data.content
    if data.category_id:
        blog.category = await Category.filter(id=data.category_id).first()
    if data.image:
        blog.image = await upload_images(data.image, data.title.replace(" ", "-").lower(), "blogs")
    if data.tags:
        blog.tags = data.tags
    await blog.save()
    return {"message": "Blog updated successfully"}

@app.delete("/category/delete/{id}",response_model=dict[str,str])
async def  category_delete(id:str ,  current_user:verify_token=Depends(verify_token)):
   await Category.filter(id=id).delete()
   return {"message": "Deleted succesfully"}


