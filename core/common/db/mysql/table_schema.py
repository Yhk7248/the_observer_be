from sqlalchemy import Column, String, DATETIME, func
from datetime import datetime

from core.common.db.mysql.settings import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(String(50), primary_key=True, index=True)
    password = Column(String(50))
    name = Column(String(50))
    birth_date = Column(DATETIME, nullable=True, default=None)
    addr = Column(String(255), nullable=True, default=None)
    phone = Column(String(50), nullable=True, default=None)
    email = Column(String(255), unique=True, index=True)
    personal_key = Column(String(255), unique=True, index=True)
    member_no = Column(String(255), unique=True, index=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    login_time = Column(DATETIME, nullable=True, default=None, onupdate=datetime.now())
