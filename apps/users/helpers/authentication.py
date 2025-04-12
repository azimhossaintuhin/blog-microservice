from  jose import JWTError, jwt
from  passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from  fastapi.security import OAuth2PasswordBearer
from  datetime import datetime, timedelta
from models import User
import uuid

ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "e4a9f7b1c8d7e2f3c4b5a6d7e8f9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",scheme_name="JWT")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str):
    return pwd_context.hash(password)

def  validate_password(password:str,hashed_password:str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data:dict,expires:datetime , refresh:bool = False):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires) if  expires else ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire}) 
    to_encode.update({"refresh": refresh})
    to_encode.update({"iat": datetime.now()})
    to_encode.update({"jti": str(uuid.uuid4())})
    to_encode.update({"user": data.get("user")})
    to_encode.update({"role": data.get("role" ,None)})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY ,algorithm=ALGORITHM)
    return encode_jwt

def decode_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def blacklistToekn(token:str=Depends(oauth2_scheme)):
    print("Token:", token)  # Debugging: Check the token being blacklisted
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        if payload:
            payload["exp"] = datetime.now() + timedelta(minutes=0)
            token = create_access_token(payload, 0)
            print("Blacklisted token:", token) 
            print("balcklisted token value", decode_token(token))# Debugging: Check the blacklisted token
        print(payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        username: str = payload.get("user")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    print("Decoded user:", username)  # Debugging: Check decoded username
    
    user = await User.get_or_none(username=username)
    if user is None:
        raise credentials_exception
    
    return user
