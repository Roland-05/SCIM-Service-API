from pydantic import Field 
from typing import Optional
from datetime import datetime
from app.schemas.api_base import APIBase


#API Sub-Schema

class NameScim(APIBase):
    formatted: Optional[str] = None
    family_name: str
    given_name: str
    middle_name: Optional[str] = None 
    honorific_prefix: Optional[str] = None
    honorific_suffix: Optional[str] = None

class EmailScim(APIBase):
    value:str
    display:Optional[str] = None
    type: Optional[str] = None
    primary: Optional[bool] = None

    #Output/ GET
class MetaScim(APIBase):
    
    resource_type: str
    created: datetime
    last_modified: datetime 
    version: Optional[str] = None
    location: Optional[str] = None

class AddressScim(APIBase):
    # All fields are optional
    formatted: Optional[str] = None
    street_address: Optional[str] = None
    locality: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None
    primary: Optional[bool] = None # Defaulting to None/NULL in DB

class ManagerScim(APIBase):
    value: Optional[str] = None
    ref: Optional[str] = Field(default=None, alias="$ref")
    display_name: Optional[str] = None


class PhoneNumberScim(APIBase):
    value: str 
    display: Optional[str] = None
    type: Optional[str] = None

class PhotoScim(APIBase):
    value: str
    type: Optional[str] = None

class ImScim(APIBase):
    value: str
    type: Optional[str] = None

class RoleScim(APIBase):
    value: str

class EntitlementScim(APIBase):
    value: str


class GroupRefScim(APIBase):
    value: str
    ref: Optional[str] = Field(default=None, alias="$ref")
    display: Optional[str] = None
