from fastapi import FastAPI

from app.db import Base, engine
from app import models
from app.routers.products import router as products_router
from app.routers.reviews import router as reviews_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 헬스체크 엔드포인트
@app.get("/health")
def health():
    return {"status": "ok"}

# 라우터 등록
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(reviews_router, prefix="/reviews", tags=["Reviews"])

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발 단계)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
