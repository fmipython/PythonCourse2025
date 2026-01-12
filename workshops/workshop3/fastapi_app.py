"""
FastAPI REST API Application
Demonstrates CRUD operations with authentication using FastAPI
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from contextlib import asynccontextmanager
from db import DatabaseService
import db_models


# ==================== Pydantic Models (Request/Response Schemas) ====================


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime


class PublicationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PublicationUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)


class PublicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime


# ==================== Application Setup ====================


_db_instance = DatabaseService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # startup
    await _db_instance.create_tables()

    try:
        yield
    finally:
        # shutdown
        await _db_instance.close()


app = FastAPI(
    title="Workshop 3 - FastAPI",
    description="REST API with CRUD operations and authentication",
    version="1.0.0",
    lifespan=lifespan,
)

security = HTTPBasic()  # за проектите проучете нещо по-сигурно като `HTTPBearer`


# ==================== Dependency Injection ====================


async def get_db() -> DatabaseService:
    """Dependency that provides database service instance"""
    return _db_instance


# ==================== Authentication ====================


async def require_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: DatabaseService = Depends(get_db),
) -> db_models.User:
    """Dependency to get and authenticate current user"""
    user = await db.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


async def require_admin_user(
    current_user=Depends(require_current_user),
) -> db_models.User:
    """Dependency to get and verify admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )
    return current_user


# ==================== USER ENDPOINTS ====================


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate, db: DatabaseService = Depends(get_db)):
    """Create a new user"""
    username, email, password = user_data.username, user_data.email, user_data.password

    user_with_username = await db.get_user_by_username(username)
    if user_with_username:
        raise HTTPException(
            status_code=400,
            detail=f"User with username {username} already exists",
        )

    user_with_email = await db.get_user_by_email(email)
    if user_with_email:
        raise HTTPException(
            status_code=400,
            detail=f"User with email {email} already exists",
        )

    new_user = await db.create_user(
        username=username,
        email=email,
        password=password,
        is_admin=False,  # always create non-admin users
    )

    return UserResponse.model_validate(new_user)


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user=Depends(require_current_user),
    db: DatabaseService = Depends(get_db),
):
    """Get user by ID"""
    user = await db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)


@app.get("/users", response_model=list[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user=Depends(require_admin_user),
    db: DatabaseService = Depends(get_db),
):
    """Get all users with pagination (admin only)"""
    users = await db.get_all_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user=Depends(require_current_user),
    db: DatabaseService = Depends(get_db),
):
    """Update user (own profile or admin can update any)"""
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    user = await db.update_user(user_id, **update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@app.delete("/users/{user_id}", status_code=200)
async def delete_user(
    user_id: int,
    current_user=Depends(require_current_user),
    db: DatabaseService = Depends(get_db),
):
    """Delete user (own account or admin can delete any)"""
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")

    success = await db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# ==================== PUBLICATION ENDPOINTS ====================


# POST /publications

# GET /publications/{publication_id}

# GET /publications?owner_id=&skip=&limit=

# PUT /publications/{publication_id}

# DELETE /publications/{publication_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
