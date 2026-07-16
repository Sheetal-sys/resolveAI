from typing import cast

from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.modules.role.models import Role
from app.modules.tenant.models import TenantUser
from app.modules.user.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # User queries
    # ---------------------------------------------------------

    def get_user_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_user_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def list_users_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> tuple[list[tuple[User, TenantUser, Role]], int]:

        query = (
            self.db.query(User, TenantUser, Role)
            .join(
                TenantUser,
                TenantUser.user_id == User.id,
            )
            .join(
                Role,
                Role.id == TenantUser.role_id,
            )
            .filter(
                TenantUser.tenant_id == tenant_id,
            )
        )

        if search:
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    User.first_name.ilike(search_value),
                    User.last_name.ilike(search_value),
                    User.email.ilike(search_value),
                    Role.name.ilike(search_value),
                )
            )

        total = query.count()

        records = cast(
            list[tuple[User, TenantUser, Role]],
            (
                query.order_by(User.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            ),
        )

        return records, total

    def get_user_by_id_and_tenant(
        self,
        user_id: int,
        tenant_id: int,
    ) -> tuple[User, TenantUser, Role] | None:
        record = (
        self.db.query(User, TenantUser, Role)
        .join(
            TenantUser,
            TenantUser.user_id == User.id,
        )
        .join(
            Role,
            Role.id == TenantUser.role_id,
        )
        .filter(
            User.id == user_id,
            TenantUser.tenant_id == tenant_id,
        )
        .first()
    )

        return cast(
        tuple[User, TenantUser, Role] | None,
        record,
    )
    def update_user(
       self,
       user: User,
    ) -> User:
        self.db.add(user)
        self.db.flush()

        return user
 
    def update_user_password(
        self,
        user: User,
        password_hash: str,
    ) -> User:
      user.password_hash = password_hash

      self.db.add(user)
      self.db.flush()

      return user
    
    
    # -------------------------------------------------
    # Role queries
    # ---------------------------------------------------------

    def get_role_by_name(self, role_name: str) -> Role | None:
        return (
            self.db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

    # ---------------------------------------------------------
    # Tenant membership queries
    # ---------------------------------------------------------

    def get_tenant_user(
        self,
        tenant_id: int,
        user_id: int,
    ) -> TenantUser | None:
        return (
            self.db.query(TenantUser)
            .filter(
                TenantUser.tenant_id == tenant_id,
                TenantUser.user_id == user_id,
            )
            .first()
        )
    
    def update_tenant_user_role(
        self,
        tenant_user: TenantUser,
        role_id: int,
    ) -> TenantUser:
         tenant_user.role_id = role_id
         self.db.add(tenant_user)
         self.db.flush()

         return tenant_user
    
    def update_tenant_user_status(
        self,
        tenant_user: TenantUser,
        is_active: bool,
    ) -> TenantUser:
         tenant_user.is_active = is_active

         self.db.add(tenant_user)
         self.db.flush()

         return tenant_user

    def create_tenant_user(
        self,
        tenant_id: int,
        user_id: int,
        role_id: int,
    ) -> TenantUser:
        tenant_user = TenantUser(
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role_id,
            is_active=True,
        )

        self.db.add(tenant_user)
        self.db.flush()

        return tenant_user


    def delete_tenant_user(
        self,
        tenant_user: TenantUser,
    ) -> None:
        self.db.delete(tenant_user)
        self.db.flush()
        
    # ---------------------------------------------------------
    # Transaction handling
    # ---------------------------------------------------------

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, record: object) -> None:
        self.db.refresh(record)