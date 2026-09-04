"""
User Pydantic Schemas — Day 3
Data validation and serialization for User & Auth request/response payloads.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Unique user email address", json_schema_extra={"example": "investor@example.com"})
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$", json_schema_extra={"example": "johndoe"})
    full_name: Optional[str] = Field(None, max_length=100, json_schema_extra={"example": "John Doe"})


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, json_schema_extra={"example": "SecurePass123!"})


class UserLogin(BaseModel):
    username_or_email: str = Field(..., json_schema_extra={"example": "investor@example.com"})
    password: str = Field(..., json_schema_extra={"example": "SecurePass123!"})


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)


class UserOut(UserBase):
    id: uuid.UUID
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(1800, description="Token validity duration in seconds")
    user: UserOut


class TokenRefresh(BaseModel):
    refresh_token: str
