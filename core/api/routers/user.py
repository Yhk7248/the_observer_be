from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.common.db.mysql.settings import get_db
from core.api.schema.user import CreateUserRequest
from core.common.db.mysql.services import create_user_account

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not Found"}}
)


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data, db)
    payload = {
        "message": "User account has been successfully created."
    }
    return JSONResponse(content=payload)
