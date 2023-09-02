from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Dict
import uuid

app = FastAPI()

users_db: Dict[str, Dict] = {}
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

sessions_db: Dict[str, str] = {}

class UserCreate(BaseModel):
    username: str
    password: str
    repeat_password: str

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)

def create_access_token(username: str):
    token = str(uuid.uuid4())
    sessions_db[token] = username
    return token

@app.post("/register", response_model=User)
async def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    if user.password != user.repeat_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    hashed_password = password_hasher.hash(user.password)
    user_data = UserInDB(username=user.username, hashed_password=hashed_password)
    users_db[user.username] = user_data.dict()
    return User(username=user.username)

@app.post("/login", response_model=str)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    token = create_access_token(user.username)
    return token

@app.post("/logout")
async def logout(token: str):
    if token not in sessions_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
    
    del sessions_db[token]
    return {"message": "Logged out"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
