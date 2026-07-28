# CareerOS - AI-Powered Career Operating System

## Architecture

CareerOS follows **Clean Architecture** with **Domain-Driven Design** principles:

```
├── backend/                    # FastAPI Backend
│   ├── src/
│   │   ├── domain/            # Domain Layer (Entities, Value Objects)
│   │   ├── application/       # Application Layer (Services, DTOs, Use Cases)
│   │   ├── infrastructure/    # Infrastructure Layer (DB, External Services)
│   │   ├── presentation/      # Presentation Layer (API Routes, Middleware)
│   │   └── shared/           # Shared Utilities
│   ├── tests/
│   ├── alembic/
│   └── Dockerfile
├── frontend/                   # NextJS 15 Frontend
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── hooks/
│   │   └── types/
│   └── Dockerfile
├── docker-compose.yml
├── nginx/
└── terraform/
```

## Phase 1 Deliverables

- ✅ Complete folder structure following Clean Architecture
- ✅ PostgreSQL database schema (fully normalized)
- ✅ Docker & Docker Compose configuration
- ✅ FastAPI backend with authentication
- ✅ NextJS 15 frontend with TypeScript
- ✅ JWT Authentication with OAuth support
- ✅ Database models with SQLAlchemy 2.0
- ✅ Alembic migrations
- ✅ Basic API endpoints

## Quick Start

```bash
# Start all services
docker-compose up --build

# Access services
Frontend: http://localhost:3000
Backend API: http://localhost:8000
Swagger UI: http://localhost:8000/docs
PostgreSQL: localhost:5432
Redis: localhost:6379
```

## Tech Stack

### Backend
- Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis
- Celery, APScheduler, Playwright, Alembic, Pydantic V2
- JWT Authentication, OAuth (Google, GitHub)

### Frontend
- NextJS 15, React 19, TypeScript, TailwindCSS
- ShadCN UI, React Query, Framer Motion, Recharts

### AI
- OpenRouter integration (Claude, GPT, Gemini, DeepSeek, Qwen)
- LangChain, LangGraph, RAG, Vector Database

### Infrastructure
- Docker, GitHub Actions, Terraform
- Prometheus, Grafana, Sentry
