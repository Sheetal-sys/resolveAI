from enum import Enum


class TenantStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class SubscriptionPlan(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class RoleName(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    SUPERVISOR = "SUPERVISOR"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    CUSTOMER = "CUSTOMER"

class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class CustomerSource(str, Enum):
    WEBSITE = "WEBSITE"
    MOBILE_APP = "MOBILE_APP"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    API = "API"
    IMPORT = "IMPORT"    