from typing import Optional, Any
from app.schemas.sub_schemas import (NameScim, EmailScim, AddressScim, PhoneNumberScim, RoleScim, EntitlementScim, ManagerScim, EnterpriseExtensionScim)
from app.schemas.api_base import APIBase
from pydantic import Field


class PatchOperation(APIBase):
    op: str
    patch: Optional[str] = None
    value: Optional[Any] = None


class PatchRequest(APIBase):
    schemas: list[str] 
    operations: list[PatchOperation]

