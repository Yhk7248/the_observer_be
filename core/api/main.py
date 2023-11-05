from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 인스턴스 생성
app = FastAPI()

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
def test_root():
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    import uvicorn

    # "main" 모듈을 실행하고 개발 서버시작.
    uvicorn.run(app, host="0.0.0.0", port=8000)
