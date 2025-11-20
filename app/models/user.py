from sqlmodel import SQLModel, Field as SQLField, Relationship
from typing import Optional
from datetime import datetime

class Name(SQLModel, table = True):
    id: Optional[int] = SQLField(default=None, primary_key = True)
    formatted: Optional[str] = None
    family_name: str # required
    given_name: str # required
    middle_name: Optional[str]  = None
    honorific_prefix: Optional[str] = None
    honorific_suffix: Optional[str] = None

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id", unique=True)
    user: "User" = Relationship(back_populates="name")


class Email(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key = True)
    value: Optional[str] = None # the email address, keep optional to prevent internal crashes
    display: Optional[str] = None
    type: Optional[str] =  None
    primary: Optional[bool] = False

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="emails")

class Meta(SQLModel, table = True):
    id: Optional[int] = SQLField(default = None, primary_key=True)
    resource_type: str = "User"
    created: datetime = SQLField(default_factory=datetime.utcnow, nullable = False)
    last_modified: datetime = SQLField(default_factory=datetime.utcnow, nullable=False)
    version: Optional[str] = None
    location: Optional[str] = None # URL of resource

    # Foreign key with unique=True constraint (one Meta object per User)
    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id", unique=True)
    user: "User" = Relationship(back_populates="meta")


class Address(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)

    # Optional Fields from SCIM standard
    formatted: Optional[str] = None
    street_address: Optional[str] = None
    locality: Optional[str] = None # City/ Suburb
    region: Optional[str] = None # State/Region
    postal_code: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None # e.g. 'work', 'home'
    primary: Optional[bool] = None 

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="addresses")

class PhoneNumber(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    value: Optional[str] = None
    display: Optional[str] = None
    type: Optional[str] = None

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="phone_numbers")

# Enterprise User Schema Extension
class Manager(SQLModel, table=True):
    #Manager - complex type refers to another user
    id: Optional[int] = SQLField(default=None, primary_key=True)

    # value
    manager_user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    manager_user: "User" = Relationship() # the user ID of the manager

    ref: Optional[str] = SQLField(default=None) # URI of the manager resource
    display_name: Optional[str] = None 
    # one to one relationship
    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id", unique = True)
    user: "User" = Relationship(back_populates="manager")
    


class User(SQLModel, table = True):
    id: Optional[int] = SQLField(default = None, primary_key = True) 
    external_id: Optional[str] = None
    user_name: str = SQLField(unique=True, index=True)
    display_name: Optional[str] = None
    active: Optional[bool] = True

    # Optional fields
    locale: Optional[str] = None
    timezone: Optional[str] = None
    nick_name: Optional[str] = None
    profile_url: Optional[str] = None
    title: Optional[str] = None
    user_type: Optional[str] = None
    preferred_language: Optional[str] = None

    # required: Defines the schema URIs this resource uses
    # Includes both the Core and the Enterprise Extension Schemas
    schemas: list[str] = SQLField(
        default_factory=lambda: [
            "urn:ietf:params:scim:schemas:core:2.0:User",
            "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
        ]
    )

    # Parent side relationships
    name: Optional[Name] = Relationship(back_populates="user", cascade="all, delete") # cascade to delete child rows (prevent orphaned data)
    emails: list[Email] = Relationship(back_populates="user", cascade="all, delete-orphan") # e.g. user.emails.pop(0)
    addresses: list[Address] = Relationship(back_populates="user", cascade="all, delete-orphan")
    meta: Optional[Meta] = Relationship(back_populates="user", cascade="all, delete")
    phone_numbers: list[PhoneNumber] = Relationship(back_populates="user", cascade="all, delete-orphan")

    # enterprise
    employee_number: Optional[str] = None
    cost_center: Optional[str] = None
    organization: Optional[str] = None
    division: Optional[str] = None
    department: Optional[str] = None
    manager: Optional[Manager] = Relationship(back_populates="user", cascade="all, delete")











