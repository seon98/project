# ERP Backend (FastAPI + SQLAlchemy + Alembic)

공공기관/병원 등에서 사용할 수 있는 ERP 백엔드 스켈레톤 프로젝트입니다. FastAPI 기반의 경량 서버로 시작하여, 조직(Organization), 사용자(User), 역할(Role)의 기본 CRUD와 계층형 모델, 서비스 계층, 마이그레이션, 테스트 환경을 갖추고 있습니다.

- Python 3.11+
- FastAPI with automatic OpenAPI/Swagger
- SQLAlchemy 2.0 ORM + Alembic migrations
- 계층형 아키텍처: routes ↔ services ↔ models ↔ db, schemas
- 테스트: pytest, FastAPI TestClient, in-memory SQLite


## 목차
- 프로젝트 개요
- 기술 스택
- 프로젝트 구조
- 빠른 시작(로컬 실행)
- 환경 변수 및 설정
- 데이터베이스 및 마이그레이션(Alembic)
- API 사용법(엔드포인트 요약 및 예시)
- 개발 가이드(레이어/의존성/트랜잭션)
- 테스트 방법
- 운영/배포 고려사항
- 문제 해결(FAQ)


## 프로젝트 개요
이 프로젝트는 ERP 시스템의 기본 뼈대(Skeleton)를 제공하여, 조직/부서/사용자/권한 관리 기능을 빠르게 시작할 수 있도록 돕습니다. 실서비스 적용 전, 도메인 모델 확장 및 인증/인가, 감사 로깅, 멀티테넌시, 복잡한 워크플로우 등은 필요에 따라 추가해 주세요.

- 기본 리소스: Organizations, Users, Roles
- 라우트는 서비스 계층을 통해 DB에 접근
- 개발 모드: 앱 시작 시 테이블 자동 생성(Base.metadata.create_all)
- 운영 모드: Alembic 마이그레이션 권장


## 기술 스택
- FastAPI >= 0.116
- SQLAlchemy >= 2.0
- Alembic >= 1.13
- Pydantic >= 2.7 (v2 스타일 ConfigDict(from_attributes=True))
- Uvicorn
- Psycopg2 (PostgreSQL 연동용)
- Pytest, httpx, FastAPI TestClient


## 프로젝트 구조
```
/Users/h_cheol_98/Desktop/ERPproject
├── app
│   ├── api
│   │   └── deps.py                # 공용 의존성(예: DB 세션)
│   ├── core
│   │   └── config.py              # Settings: APP 메타데이터, DATABASE_URL 등
│   ├── db
│   │   ├── base.py                # SQLAlchemy Base 및 모델 메타데이터 등록
│   │   └── session.py             # Engine/SessionLocal 구성
│   ├── main.py                    # FastAPI 앱 팩토리/라우터 연결/CORS/Startup
│   ├── models                     # ORM 모델(조직/부서/사용자/역할)
│   │   ├── organization.py
│   │   ├── department.py
│   │   ├── role.py
│   │   └── user.py
│   ├── routes                     # API 라우트(Organizations/Users/Roles CRUD)
│   │   ├── organization.py
│   │   ├── roles.py
│   │   └── users.py
│   ├── schemas                    # Pydantic 스키마(생성/수정/조회)
│   │   ├── organization.py
│   │   ├── role.py
│   │   └── user.py
│   └── services                   # 서비스 계층(트랜잭션/도메인 로직)
│       ├── organization_service.py
│       ├── role_service.py
│       └── user_service.py
├── alembic
│   └── env.py                     # Alembic 환경 설정(Base.metadata, DB URL)
├── alembic.ini                    # Alembic 설정 파일
├── main.py                        # 최상위 런처(uvicorn app.main:app)
├── pyproject.toml                 # 의존성 및 pytest 설정
├── tests
│   ├── conftest.py                # 테스트용 DB/세션/클라이언트 설정
│   └── test_organization.py       # 조직 CRUD 플로우 테스트
├── test_main.http                 # HTTP 요청 예제(REST Client 등으로 실행)
└── uv.lock                        # uv 패키지 매니저 lock 파일
```


## 빠른 시작(로컬 실행)
1) 의존성 설치
- uv 사용(권장):
  - uv가 없다면: https://docs.astral.sh/uv/
  - 설치 후:
    - uv sync
- pip 사용:
  - python -m venv .venv && source .venv/bin/activate (Windows: .venv\Scripts\activate)
  - pip install -r requirements.txt (필요 시) 또는 pyproject.toml 기반으로 pip install .
  - 또는 수동: pip install fastapi uvicorn sqlalchemy alembic pydantic psycopg2-binary python-dotenv httpx pytest email-validator

2) 환경 변수 준비(선택)
- 기본값은 SQLite 파일(./erp.db)을 사용합니다. PostgreSQL 사용 시 DATABASE_URL을 설정하세요.

3) 서버 실행
- uv 사용: uv run uvicorn app.main:app --reload
- pip/venv 사용: uvicorn app.main:app --reload

4) 문서/테스트 확인
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: GET /


## 환경 변수 및 설정
app/core/config.py의 Settings(BaseModel)에서 다음 항목을 제공합니다.
- APP_NAME: 기본 "ERP Backend"
- APP_VERSION: 기본 "0.1.0"
- APP_DESCRIPTION: OpenAPI 설명
- DATABASE_URL: 기본 sqlite:///./erp.db (CI 환경에서는 메모리 SQLite)
- SQLALCHEMY_ECHO: true/false (SQL 로그)

예시(.env):
```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/erp
SQLALCHEMY_ECHO=false
```

환경변수를 설정하면 Alembic도 이를 참조하여 마이그레이션 시 동일한 DB에 적용됩니다(alembic/env.py에서 Settings를 불러옵니다).


## 데이터베이스 및 마이그레이션(Alembic)
- 개발 단계: 앱 시작 시 Base.metadata.create_all(bind=engine)로 테이블 자동 생성
- 운영 단계: 스키마 변경은 Alembic 마이그레이션 사용 권장

초기 마이그레이션 생성:
```
alembic revision --autogenerate -m "init"
```
마이그레이션 적용/롤백:
```
alembic upgrade head
alembic downgrade -1
```
Alembic 설정:
- alembic.ini: 기본 sqlalchemy.url은 sqlite:///./erp.db 이나, env.py에서 Settings.DATABASE_URL로 덮어씁니다.
- alembic/env.py: Base.metadata를 target_metadata로 설정(자동 감지용)


## API 사용법(엔드포인트 요약 및 예시)
기본 URL: http://127.0.0.1:8000

공통 사항:
- Content-Type: application/json
- Swagger UI에서 요청/응답 스키마와 Try it out을 통해 직접 호출 가능

### 1) Organizations
- POST /organizations/ — 조직 생성
- GET /organizations/ — 조직 목록
- GET /organizations/{org_id} — 조직 상세
- PUT /organizations/{org_id} — 조직 수정
- DELETE /organizations/{org_id} — 조직 삭제

요청/응답 예시:
- 생성 요청:
엔드포인트: POST /organizations/
요청 바디(JSON):
```json
{
  "name": "Seoul General Hospital",
  "description": "Public healthcare"
}
```
- 성공(201 Created) 응답:
```json
{
  "id": 1,
  "name": "Seoul General Hospital",
  "description": "Public healthcare",
  "created_at": "2025-09-05T09:00:00",
  "updated_at": "2025-09-05T09:00:00"
}
```
- 중복 이름 생성 시(400): { "detail": "Organization name already exists" }
- 미존재 조회(404): { "detail": "Organization not found" }

### 2) Roles
- POST /roles/
- GET /roles/
- GET /roles/{role_id}
- PUT /roles/{role_id}
- DELETE /roles/{role_id}

예시 요청:
엔드포인트: POST /roles/
요청 바디(JSON):
```json
{
  "name": "admin",
  "description": "Full access"
}
```
- 중복 이름 생성 시(400): { "detail": "Role name already exists" }
- 미존재 조회(404): { "detail": "Role not found" }

### 3) Users
- POST /users/
- GET /users/
- GET /users/{user_id}
- PUT /users/{user_id}
- DELETE /users/{user_id}

예시 요청:
엔드포인트: POST /users/
요청 바디(JSON):
```json
{
  "email": "alice@example.com",
  "full_name": "Alice",
  "password": "secret123",
  "organization_id": 1,
  "department_id": null
}
```
- 중복 이메일 생성 시(400): { "detail": "Email already registered" }
- 미존재 조회(404): { "detail": "User not found" }

참고:
- 비밀번호는 데모 목적으로 sha256으로 해시됩니다(app/services/user_service.py). 실제 운영에서는 bcrypt/Argon2(passlib 등)를 사용하세요.
- User.roles 연관은 모델에 정의되어 있으나, 본 스켈레톤에는 역할 배정/해제 API는 포함되어 있지 않습니다(필요 시 확장).

### REST Client 예시 파일
- test_main.http를 VS Code REST Client, IntelliJ HTTP Client 등에서 열어 순차 호출을 시도할 수 있습니다.


## 개발 가이드
### 레이어드 아키텍처
- routes (FastAPI APIRouter): 요청 유효성, 예외 처리, 서비스 호출
- services: 트랜잭션 경계(commit/refresh/delete), 도메인 로직, 쿼리 구성
- models: SQLAlchemy ORM 엔티티(Organization/Department/User/Role, 다대다 user_roles)
- schemas: Pydantic v2 스키마(생성/수정/조회 분리, from_attributes=True)
- db: Base/engine/session 구성, get_db 의존성 제공

### 의존성 주입
- app/api/deps.py의 get_db()를 통해 요청마다 세션을 열고 응답 후 닫습니다.
- tests에서는 dependency_overrides를 통해 테스트 세션을 주입합니다.

### 트랜잭션/세션
- 서비스 계층에서 db.add/commit/refresh 를 통해 트랜잭션을 완료합니다.
- 읽기 전용 작업은 select + scalars().all() 사용(2.0 스타일).


## 테스트 방법
- 테스트 DB: in-memory SQLite(StaticPool) 공유로 세션 간 데이터 유지
- 실행:
```
pytest -q
```
- 포함 테스트: tests/test_organization.py (기본 CRUD 플로우)
- conftest.py에서 FastAPI TestClient와 세션 오버라이드 로직 확인 가능


## 운영/배포 고려사항
- 데이터베이스: SQLite는 개발/테스트용, 운영은 PostgreSQL 등 RDB 권장
- 마이그레이션: 모든 스키마 변경은 Alembic revision --autogenerate 로 관리
- 비밀번호 해시: bcrypt/argon2 등 강력한 해시로 교체
- CORS: app/main.py의 CORSMiddleware에서 allow_origins를 서비스 도메인으로 제한
- 로깅/모니터링: Uvicorn/ASGI 로깅, APM, 구조화 로그(JSON) 고려
- 설정 관리: .env 또는 시크릿 매니저 사용, DATABASE_URL/SECRET_KEY 등 중요 값 분리
- 자동 테이블 생성 비활성화: 운영에서는 startup 훅의 create_all 사용 지양, 마이그레이션만 사용


## 문제 해결(FAQ)
- 서버는 떠 있으나 스키마가 없다고 나옵니다.
  - 개발 모드라면 앱 시작 시 자동 생성됩니다. 운영 모드라면 alembic upgrade head 를 실행하세요.
- PostgreSQL 연결 오류(psycopg2):
  - DATABASE_URL이 올바른지, 포트/방화벽/권한을 확인하세요.
- 이메일 유효성 오류:
  - Pydantic EmailStr를 사용하므로 RFC 유효성 검사에 맞는 이메일을 사용하세요.
- 테스트 시 데이터가 사라져요:
  - in-memory SQLite는 프로세스 메모리를 사용합니다. StaticPool을 사용하므로 같은 프로세스/세션 공유를 전제로 합니다.


## 라이선스
- 내부 프로젝트용 스켈레톤으로 별도 라이선스 명시가 없다면 사내 표준을 따르세요.



## 프론트엔드(데모) — Vue 3 (CDN)
이 프로젝트에는 FastAPI 백엔드와 연동되는 간단한 프론트엔드 데모가 포함되어 있습니다.

- 경로: http://127.0.0.1:8000/frontend/
- 프레임워크: Vue 3 (CDN, 번들링/빌드 불필요)
- 기능: Organizations 리소스 목록 조회, 생성, 수정, 삭제
- 연동 API: /organizations/ (POST/GET/PUT/DELETE)

사용 방법
1) 서버 실행
- uv 사용: uv run uvicorn app.main:app --reload
- 또는: uvicorn app.main:app --reload

2) 브라우저에서 접속
- http://127.0.0.1:8000/frontend/
- 상단 입력 폼으로 조직을 생성하고, 표에서 즉시 수정/삭제할 수 있습니다.

구현 메모
- 정적 파일 제공: app/main.py에서 아래와 같이 StaticFiles를 마운트합니다.
  - app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
- 동일 오리진으로 제공되므로 CORS 설정 없이도 API 호출이 가능합니다.
- 프론트엔드 코드는 단일 파일(frontend/index.html)로 구성되어 유지보수가 간단합니다.

문제 해결(Frontend)
- 404 Not Found (GET /frontend/): frontend/index.html 파일이 존재하는지, main.py에서 StaticFiles 마운트가 되어 있는지 확인하세요.
- API 호출 에러: 백엔드가 실행 중인지, 콘솔/네트워크 탭에서 상태 코드와 응답 본문(detail)을 확인하세요.
