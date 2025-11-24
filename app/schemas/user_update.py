
from typing import Optional
from app.schemas.sub_schemas import (NameScim, EmailScim, AddressScim, PhoneNumberScim, RoleScim, EntitlementScim, ManagerScim, EnterpriseExtensionScim)
from app.schemas.api_base import APIBase
from pydantic import Field

class UserUpdate(APIBase):

    external_id: Optional[str] = None
    user_name: Optional[str] = None
    display_name: Optional[str] = None
    active: Optional[bool] = True

    locale: Optional[str] = None
    timezone: Optional[str] = None
    nick_name: Optional[str] = None
    profile_url: Optional[str] = None
    title: Optional[str] = None
    user_type: Optional[str] = None
    preferred_language: Optional[str] = None

    name: Optional[NameScim] = None
    emails: Optional[list[EmailScim]] = None
    addresses: Optional[list[AddressScim]] = None
    phone_numbers: Optional[list[PhoneNumberScim]] = None

    roles: Optional[list[RoleScim]] = None
    entitlements: Optional[list[EntitlementScim]] = None
    manager: Optional[ManagerScim] = None

    # Enterprise
    enterprise_extension: Optional[EnterpriseExtensionScim] = Field(
        default=None,
        alias="urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
    )