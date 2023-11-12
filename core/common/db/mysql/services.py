from .table_schema import UserModel
from .manager import MysqlManager
from core.common.helper.jwt_helper import get_password_hash

from fastapi.exceptions import HTTPException
from datetime import datetime


async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")
    new_user = UserModel(
        id=data.id,
        password=get_password_hash(data.password),
        name=data.name,
        birth_date=data.birth_date,
        addr=data.addr,
        phone=data.phone,
        email=data.email,
        personal_key=data.personal_key,
        member_no=data.member_no,
        created_at=datetime.now(),
        login_time=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
