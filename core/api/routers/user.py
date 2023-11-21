from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.common.db.mysql.settings import get_db
from core.common.helper.jwt_helper import oauth2_scheme
from core.api.schema.user import CreateUserRequest, UserResponse
from core.common.db.mysql.services import create_user_account

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not Found"}}
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data, db)
    payload = {
        "message": "User account has been successfully created."
    }
    return JSONResponse(content=payload)


@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user
