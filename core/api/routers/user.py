from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.db.mysql.settings import get_db
from core.api.schema.user import CreateUserRequest

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not Found"}}
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    pass
