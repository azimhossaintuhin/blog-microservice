from fastapi import FastAPI, Depends ,HTTPException
from contextlib import asynccontextmanager
from tortoise import Tortoise
from config.Database import TORTOISE_ORM
from models import Comment, Reply
from helpers.blog_exsits import blog_exists
from helpers.authentication import get_current_user
from schemas import CommentOut ,CommentIn ,ReplyIn,ReplyOut,CommentUpdateOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app = FastAPI(
    lifespan=lifespan,
    title="Comments Service",
    description="This is a comments service for Blog Microservice",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to the comments service"}

@app.get("/comments/{blog_id}",response_model=list[CommentOut] | dict[str, str])
async def get_comments(blog_id: str, blog=Depends(blog_exists)):
    comments = await Comment.filter(blog_id=blog_id).prefetch_related("replies")
    if not comments:
        return {"message": "No comments found"}

    comment_data = []
    for comment in comments:
        replies = await comment.replies.all()
        comment_data.append({
            "id": comment.id,
            "blog_id": comment.blog_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": comment.created_at,
            "replies": [{
                "id": reply.id,
                "comment_id": reply.comment_id,
                "user_id": reply.user_id,
                "content": reply.content,
                "created_at": reply.created_at
            } for reply in replies]
        })

    return comment_data

@app.post("/comments/create/{blog_id}", response_model=CommentOut | dict[str, str])
async def create_comment(
    blog_id: str,
    comment: CommentIn,
    current_user=Depends(get_current_user),
    current_blog=Depends(blog_exists)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not current_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    comment_obj = await Comment.create(
        blog_id=blog_id,
        user_id=current_user.get("id"),
        content=comment.content
    )

    # Load replies explicitly (even though it's empty initially)
    await comment_obj.fetch_related("replies")

    return comment_obj

@app.put("/comments/update/{comment_id}", response_model=CommentUpdateOut | dict[str, str])
async def update_comment(
    comment_id: str,
    comment: CommentIn,
    current_user=Depends(get_current_user),
  
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    comment_obj = await Comment.get_or_none(id=comment_id)
    if not comment_obj:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment_obj.user_id != current_user.get("id" ):
        raise HTTPException(status_code=403, detail="Forbidden")

    comment_obj.content = comment.content
    await comment_obj.save()
    
  
    
    return comment_obj




@app.get("/comments/replies/{comment_id}", response_model= list[ReplyOut] | dict[str, str])
async def get_replies(comment_id: str):
    replies = await Reply.filter(comment_id=comment_id).all()
    if not replies:
        return {"message": "No replies found"}

    return replies


@app.delete("/comments/delete/{comment_id}", response_model=dict[str, str])
async def delete_comment(
    comment_id: str,
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Forbidden")

    await comment.delete()
    return {"message": "Comment deleted successfully"}





@app.get("/comments/replies/{comment_id}", response_model=list[ReplyOut] | dict[str, str])
async def get_replies(
    comment_id: str,
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    replies = await Reply.filter(comment_id=comment_id).all()
    if not replies:
        return {"message": "No replies found"}

    return replies

@app.post("/comments/replies/create/{comment_id}", response_model=ReplyOut | dict[str, str])
async def create_reply(
    comment_id: str,
    reply: ReplyIn,
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    reply_obj = await Reply.create(
        comment_id=comment_id,
        user_id=current_user.get("id"),
        content=reply.content
    )

    return reply_obj


@app.put("/comments/replies/update/{reply_id}", response_model=ReplyOut | dict[str, str])
async def update_reply(
    reply_id: str,
    reply: ReplyIn,
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    reply_obj = await Reply.get_or_none(id=reply_id)
    if not reply_obj:
        raise HTTPException(status_code=404, detail="Reply not found")

    if reply_obj.user_id != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Forbidden")

    reply_obj.content = reply.content
    await reply_obj.save()

    return reply_obj

@app.delete("/comments/replies/delete/{reply_id}", response_model=dict[str, str])
async def delete_reply(
    reply_id: str,
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    reply = await Reply.get_or_none(id=reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    if reply.user_id != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Forbidden")

    await reply.delete()
    return {"message": "Reply deleted successfully"}