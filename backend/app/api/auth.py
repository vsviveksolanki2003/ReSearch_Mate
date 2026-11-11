"""API routes for user registration, login, and workspace management."""
import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from backend.app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

_USERS_DB: Dict[str, Dict[str, Any]] = {}

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegister):
    """Register a new researcher account."""
    if payload.email in _USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    user_id = f"user-{uuid.uuid4().hex[:8]}"
    workspace_id = f"ws-{uuid.uuid4().hex[:8]}"

    hashed = hash_password(payload.password)
    user_record = {
        "id": user_id,
        "email": payload.email,
        "username": payload.username,
        "password_hash": hashed,
        "workspace_id": workspace_id
    }
    _USERS_DB[payload.email] = user_record

    token = create_access_token({"sub": user_id, "email": payload.email, "workspace_id": workspace_id})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user_id,
            email=payload.email,
            username=payload.username,
            workspace_id=workspace_id
        )
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(payload: UserLogin):
    """Authenticate researcher and issue JWT token."""
    user = _USERS_DB.get(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token({"sub": user["id"], "email": user["email"], "workspace_id": user["workspace_id"]})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            username=user["username"],
            workspace_id=user["workspace_id"]
        )
    )
