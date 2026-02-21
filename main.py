from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import timedelta
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import create_tables, create_user, get_all_users, update_user, get_user_by_email, User as DBUser
from auth import authenticate_user, create_access_token, get_password_hash, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate, UserResponse, UserLogin, Token

app = FastAPI(title="Health Insurance API", version="1.0.0")

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to Health Insurance API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Check if user already exists
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = create_user(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password,
        income_profile=user.income_profile,
        coverage=user.coverage
    )
    
    return UserResponse(
        id=db_user.id,
        full_name=db_user.full_name,
        email=db_user.email,
        income_profile=db_user.income_profile,
        coverage=db_user.coverage,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: DBUser = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        income_profile=current_user.income_profile,
        coverage=current_user.coverage,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@app.get("/users", response_model=List[UserResponse])
async def get_all_users_endpoint(current_user: DBUser = Depends(get_current_user)):
    users = get_all_users()
    return [
        UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            income_profile=user.income_profile,
            coverage=user.coverage,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) for user in users
    ]

@app.put("/users/me", response_model=UserResponse)
async def update_user_endpoint(
    user_update: UserCreate,
    current_user: DBUser = Depends(get_current_user)
):
    # Update user fields
    hashed_password = get_password_hash(user_update.password) if user_update.password else None
    
    updated_user = update_user(
        user_id=current_user.id,
        full_name=user_update.full_name,
        income_profile=user_update.income_profile,
        coverage=user_update.coverage,
        password_hash=hashed_password
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=updated_user.id,
        full_name=updated_user.full_name,
        email=updated_user.email,
        income_profile=updated_user.income_profile,
        coverage=updated_user.coverage,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

if __name__ == "__main__":
    import hypercorn
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    
    config = Config()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    config.bind = [f"{host}:{port}"]
    asyncio.run(serve(app, config))
