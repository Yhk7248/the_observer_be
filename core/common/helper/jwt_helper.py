from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from core.common.loader.config_loader import ConfigLoader
from core.common.db.mysql.table_schema import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int


async def create_access_token(data, expiry: timedelta):
    payload: dict = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, ConfigLoader().config.JWT_SECRET, algorithm=ConfigLoader().config.JWT_ALGORITHM)


async def create_refresh_token(data):
    return jwt.encode(data, ConfigLoader().config.JWT_SECRET, algorithm=ConfigLoader().config.JWT_ALGORITHM)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.id == data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # _verify_user_access(user=user)

    return await _get_user_token(user=user)   # return access token and refresh token


def _verify_user_access(user: UserModel):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive. Please contact support.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_verified:
        # Trigger user account verification email
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified. We have resend the account verification email.",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def _get_user_token(user: UserModel, refresh_token=None):
    payload = {"id": user.id}
    access_token_expiry = timedelta(minutes=ConfigLoader().config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )
