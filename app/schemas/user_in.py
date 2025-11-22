from app.schemas.sub_schemas import (NameScim, EmailScim, AddressScim, PhoneNumberScim, RoleScim, EntitlementScim, ManagerScim, EnterpriseExtensionScim)
from pydantic import Field
from app.schemas.api_base import APIBase
from typing import Optional
# Main API Schemas

# POST request
# Define the expected JSON input, which does not include system-generated IDs
class UserCreate(APIBase):
    external_id: Optional[str] = None
    user_name: str
    display_name: Optional[str] = None
    active: Optional[bool] = True

# Simple Optional SCIM Attributes 
    locale: Optional[str] = None
    timezone: Optional[str] = None
    nick_name: Optional[str] = None
    profile_url: Optional[str] = None
    title: Optional[str] = None
    user_type: Optional[str] = None
    preferred_language: Optional[str] = None


    # Nested Schemas

    name: Optional[NameScim] = None
    # use validation constraint mandated by the SCIM RFC
    emails: list[EmailScim] = Field(min_items=1) # SCIM requires at least one email
    addresses: list[AddressScim] = Field(default_factory=list)
    phone_numbers: list[PhoneNumberScim] = Field(default_factory=list)

    roles: list[RoleScim] = Field(default_factory=list)
    entitlements: list[EntitlementScim] = Field(default_factory=list)

    # Enterprise
    enterprise_extension: Optional[EnterpriseExtensionScim] = Field(
        default=None,
        alias="urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
    )

    # employee_number: Optional[str] = None
    # cost_center: Optional[str] = None
    # organization: Optional[str] = None
    # division: Optional[str] = None
    # department: Optional[str] = None
    # manager: Optional[ManagerScim] = None

