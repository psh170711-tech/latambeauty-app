from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================
# DB 연결 + Base import 필수!!
# ============================
from app.db.base import Base
from app.db.session import engine

# 🔥 사용되는 라우터
from app.routers import product_router, offer_router, review_router

app = FastAPI(
    title="LatamBeauty API",
    version="1.0.0"
)

# ============================================================
# CORS 설정
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔥 DB 테이블 자동 생성
# ============================================================
@app.on_event("startup")
def startup():
    print("📌 Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("📌 DB ready!")

# ============================================================
# 라우터 연결
# ============================================================
app.include_router(product_router.router)
app.include_router(offer_router.router)
app.include_router(review_router.router)

# ============================================================
# 기본 루트 엔드포인트
# ============================================================
@app.get("/")
def root():
    return {"message": "LatamBeauty API is running 🚀"}