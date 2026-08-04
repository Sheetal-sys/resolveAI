from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.core.config import settings
from app.database.db import Base

# ---------------------------------------------------------
# Import ALL SQLAlchemy models here.
# These imports register the models in Base.metadata.
# ---------------------------------------------------------

from app.modules.role.models import Role
from app.modules.user.models import User
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.tenant_settings.models import TenantSettings
from app.modules.customer.models import Customer
from app.modules.products.models import Product

# ---------------------------------------------------------

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """

    configuration = config.get_section(config.config_ini_section)

    if configuration is None:
     raise RuntimeError("Alembic configuration could not be loaded.")

    connectable = engine_from_config(
    configuration,
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()