# ResolveAI Backend

ResolveAI is a multi-tenant AI-powered customer support SaaS platform.

The backend is built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, and role-based access control.

---

## Current Features

### Platform Foundation

- FastAPI backend
- PostgreSQL database
- SQLAlchemy 2.0 ORM
- Alembic database migrations
- Environment-based configuration
- Modular backend architecture

### Authentication and Security

- Secure password hashing
- JWT access tokens
- Login API
- Current-user API
- Role-based access control
- Protected API endpoints

### Multi-Tenant Platform

- Tenant registration
- Tenant admin creation
- Tenant-specific memberships
- Tenant-level data isolation
- Tenant-specific user roles
- Automatic tenant settings creation

### User Management

- Create employees
- List users
- Search users
- Pagination
- View user details
- Update user details
- Change user role
- Activate or deactivate users
- Reset employee passwords
- Remove users from tenants

### Tenant Settings

- Read tenant settings
- Update tenant settings
- Company website and support details
- Time zone, language, and currency
- Business hours
- Logo URL
- AI confidence threshold
- Auto-reply configuration
- Auto-escalation configuration

---

## Technology Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Language | Python 3.11 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic |
| Authentication | JWT |
| Password Security | Passlib and bcrypt |
| Testing | Pytest |
| API Documentation | Swagger / OpenAPI |

---

## Project Structure

```text
backend/
├── app/
│   ├── core/
│   ├── database/
│   ├── infrastructure/
│   ├── modules/
│   │   ├── auth/
│   │   ├── role/
│   │   ├── tenant/
│   │   ├── tenant_settings/
│   │   └── user/
│   ├── shared/
│   └── main.py
│
├── migrations/
├── tests/
├── .env.example
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md