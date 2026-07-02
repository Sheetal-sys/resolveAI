from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.tenant.repository import TenantRepository
from app.modules.tenant.schemas import TenantRegisterRequest, TenantRegisterResponse
from app.modules.tenant.service import TenantService

router = APIRouter(
    prefix="/api/v1/tenants",
    tags=["Tenants"],
)


@router.post("/register", response_model=TenantRegisterResponse)
def register_tenant(
    request: TenantRegisterRequest,
    db: Session = Depends(get_db),
):
    repository = TenantRepository(db)
    service = TenantService(repository)

    return service.register_tenant(request)