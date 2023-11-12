from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from core.common.loader.config_loader import ConfigLoader
from core.common.db.mysql.settings import Settings
from core.api.routers.user import router as user_router
from core.api.routers.auth import router as auth_router

# FastAPI 인스턴스 생성
app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


# *로 모든 접근을 허용할 수 있다.
origins = [
    "*"
]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],  # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],  # 허용할 http header 목록을 설정할 수 있으며 Content-Type,
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
