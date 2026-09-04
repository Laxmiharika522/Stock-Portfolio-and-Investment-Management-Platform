"""
Authentication Router — Day 3
API Endpoints for User Registration, Login, Token Refresh, and Session Management.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, TokenRefresh
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
    description="Registers a new user with unique email & username, hashing their password with bcrypt.",
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await AuthService.register_user(db, user_in)
    return UserOut.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user & obtain JWT tokens",
    description="Authenticates user credentials and returns signed JWT access and refresh tokens.",
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    return await AuthService.authenticate_user(db, credentials)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Issues a fresh JWT access token using a valid refresh token.",
)
async def refresh_token(
    token_in: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.refresh_access_token(db, token_in.refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user session",
    description="Logs out the current user session.",
)
async def logout():
    return {"success": True, "message": "Successfully logged out"}

