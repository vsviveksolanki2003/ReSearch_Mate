"""Pydantic schemas for authentication and workspaces."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserRegister(BaseModel):
    email: str = Field(..., min_length=3)
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    workspace_id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
