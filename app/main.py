"""
FastAPI ERP Skeleton
- Python 3.11+
- FastAPI with automatic OpenAPI/Swagger
- SQLAlchemy ORM + Alembic migrations
- Layered architecture: routes, schemas, services, models, db

실행 예시 (개발용):
    uv run uvicorn app.main:app --reload

환경 변수:
    DATABASE_URL: 기본값 sqlite:///./erp.db (개발용)
    SQLALCHEMY_ECHO: true/false (SQL 로깅)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.routes.organization import router as org_router
from app.routes.users import router as user_router
from app.routes.roles import router as role_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    openapi_tags=[
        {"name": "Organizations", "description": "조직/부서 관리"},
        {"name": "Users", "description": "사용자(직원) 관리"},
        {"name": "Roles", "description": "권한(역할) 관리"},
        {"name": "Finance", "description": "회계/재무 관리 (추후)"},
        {"name": "Assets", "description": "자산/구매/재고 관리 (추후)"},
    ],
)

# CORS (필요 시 도메인을 설정하세요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """개발 초기 단계에서는 자동으로 테이블을 생성합니다.
    운영 단계에서는 Alembic 마이그레이션을 사용하세요.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "ERP Backend is running", "version": settings.APP_VERSION}


# 라우터 등록
app.include_router(org_router)
app.include_router(user_router)
app.include_router(role_router)

# 정적 프론트엔드 제공 (/frontend)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
