from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
import uvicorn

from core.common.helper.jwt_helper import JWTAuth
from core.common.loader.config_loader import ConfigLoader
from core.common.db.mysql.settings import Settings
from core.api.routers.user import router as guest_router, user_router
from core.api.routers.auth import router as auth_router

# FastAPI 인스턴스 생성
app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)


# *로 모든 접근을 허용할 수 있다.
origins = [
    "*"
]

# CORS 미들웨어 설정
app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuth(),
)


@app.get("/")
def health_check():
    return JSONResponse(
        content={"status": "running"}
    )


if __name__ == "__main__":
    # http://127.0.0.1:8000/docs >> 스웨거 주소
    ConfigLoader().load(path='../common/config/config.yaml')
    Settings()
    uvicorn.run(app, host="0.0.0.0", port=8000)
