"""
    user 관련 BaseModel schema
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union


class CreateUserRequest(BaseModel):
    id: str
    password: str
    name: str
    birth_date: datetime
    addr: str
    phone: str
    email: EmailStr
    personal_key: str
    member_no: str
    created_at: datetime
    # login_time: datetime


class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    registered_at: Union[None, datetime] = None
