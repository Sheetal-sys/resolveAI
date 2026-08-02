from fastapi import FastAPI

from app.modules.auth.api import router as auth_router
from app.modules.tenant.api import router as tenant_router
from app.modules.user.api import router as user_router
from app.modules.tenant_settings.api import (
    router as tenant_settings_router,
)

app = FastAPI(
    title="ResolveAI API",
    description="Multi-tenant Agentic AI Customer Support SaaS Platform",
    version="1.0.0",
)

app.include_router(tenant_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {
        "message": "ResolveAI backend is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }

app.include_router(
    tenant_settings_router,
    prefix="/api/v1",
)