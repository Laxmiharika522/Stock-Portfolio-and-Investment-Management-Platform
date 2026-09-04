"""
Users Router — Day 3
API Endpoints for User Profile Management and Password Updates.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, PasswordChange
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user profile",
    description="Retrieves profile information for the currently authenticated user.",
)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
) -> UserOut:
    return UserOut.model_validate(current_user)


@router.put(
    "/me",
    response_model=UserOut,
    summary="Update current user profile",
    description="Updates profile fields (email, username, full_name) for the authenticated user.",
)
async def update_my_profile(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    updated_user = await AuthService.update_profile(db, current_user, user_in)
    return UserOut.model_validate(updated_user)


@router.put(
    "/me/password",
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="Changes password for the currently authenticated user after verifying their old password.",
)
async def change_my_password(
    pwd_in: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await AuthService.change_password(db, current_user, pwd_in)
    return {"success": True, "message": "Password changed successfully"}
