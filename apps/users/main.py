from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from config.Databse import TORTOISE_ORM  
from tortoise import Tortoise
from schemas import UserIn, UserOut ,LoginUser,Token ,UserProfileIn ,UserProfileOut# M
from models import User , UserProfile
from helpers.authentication import *
from helpers.fileUpload import upload_images ,UPLOAD_DIRECTORY
from  fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


@asynccontextmanager
async def life_span(app: FastAPI):
 
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas() 
    yield
    await Tortoise.close_connections()  


app = FastAPI(
    lifespan=life_span
)


app.mount(f"/{UPLOAD_DIRECTORY}/", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")


@app.get("/")
async def root():
    return {"message": "Welcome to the blog user service"}


@app.post("/register", 
          response_model=UserOut,
          
          )
async def user_registration(user: UserIn):
    username = user.username
    email = user.email

   
    if await User.filter(username=username).exists() or await User.filter(email=email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or email already exists"
        )

    # Create the new user
    user_obj = await User.create(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)  
    )
  
    return await user_obj


@app.post("/login",response_model=Token, )
async def login(user: LoginUser):
    print(user)
    data = user.model_dump()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username and not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    if username:
        user_obj = await User.get_or_none(username=username)
    if email:
        user_obj = await User.get_or_none(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not validate_password(password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    access_token = create_access_token(
        data={"user": user_obj.username},
        expires=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_access_token(
        data={"user": user_obj.username},
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh=True
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@app.post("/token" )
async def toeken(form_data: OAuth2PasswordRequestForm = Depends()):
    
    data = form_data

    username = data.username

    password = data.password
    
    
    if not username :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    if username:
        user_obj = await User.get_or_none(username=username)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not validate_password(password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    access_token = create_access_token(
        data={"user": user_obj.username},
        expires=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_access_token(
        data={"user": user_obj.username},
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh=True
    )
    return {
        "access_token": access_token,
       
        "token_type": "bearer"
    }




@app.get("/users", response_model=list[UserOut])
async def get_all_users(current_user: User = Depends(get_current_user)):
    print(current_user)
    users = await User.all()
    return users


@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: str, get_current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: str, get_current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await user.delete()
    return {"message": "User deleted successfully"}



@app.get("/user", response_model=UserOut)
async def get_current_user_data(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/update/profile/", response_model=UserProfileOut)
async def profile_update(user_info:UserProfileIn=Depends(UserProfileIn.as_form),current_user: User = Depends(get_current_user) ):
    try:
        profile = await UserProfile.get_or_none(user_id= current_user.id)
        if  not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            user__username
        
        file_name = current_user.username
        profile = await UserProfile.filter(user_id=current_user.id).update(
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            phone=user_info.phone,
            address=user_info.address,
            profile_picture=await upload_images(user_info.profile_picture, file_name, "profile_pictures")
        )
        profile = await UserProfile.get_or_none(user_id=current_user.id)
        return profile
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
   
    
    