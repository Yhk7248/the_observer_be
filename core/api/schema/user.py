"""
    user 관련 BaseModel schema
"""
from pydantic import BaseModel
from datetime import datetime


class CreateUserRequest(BaseModel):
    id: str
    password: str
    name: str
    birth_date: datetime
    addr: str
    phone: str
    email: str
    personal_key: str
    member_no: str
    created_at: datetime
    # login_time: datetime
