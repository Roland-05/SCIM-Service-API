from sqlmodel import SQLModel, Session, Field as SQLField, Relationship
from typing import Optional
from datetime import datetime

class Name(SQLModel, table = True):
    id: Optional[int] = SQLField(default=None, primary_key = True)
    formatted: Optional[str]
    familyName: str # required
    givenName: str # required
    middleName: Optional[str] 
    honorificPrefix: Optional[str]
    honorificSuffix: Optional[str]

    user_id: int | None = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="name")


class Email(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key = True)
    value: str # the email address
    display: Optional[str]
    type: Optional[str]
    primary: Optional[bool] = False

    user_id: int | None = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="emails")

class Meta(SQLModel, table = True):
    id: int | None = SQLField(default = None, primary_key=True)
    resourceType: str = "User"
    created: datetime = SQLField(default_factory=datetime.utcnow, nullable = False)
    lastModified: datetime = SQLField(default_factory=datetime.utcnow, nullable=False)
    version: Optional[str] = None
    location: Optional[str] # URL of resource

    # Foreign key with unique=True constraint (one Meta object per User)
    user_id: int | None = SQLField(default=None, foreign_key="user.id", unique=True)
    user: "User" = Relationship(back_populates="meta")


class Address(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)

    # Optional Fields from SCIM standard
    formatted: Optional[str] = None
    streetAddress: Optional[str] = None
    locality: Optional[str] = None # City/ Suburb
    region: Optional[str] = None # State/Region
    postalCode: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None # e.g. 'work', 'home'
    primary: Optional[bool] = None 

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="addresses")

class phoneNumber(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    value: str = None
    display: Optional[str] = None
    type: Optional[str] = None

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="phoneNumbers")

# Enterprise User Schema Extension
class Manager(SQLModel, table=True):
    #Manager - complex type refers to another user
    id: Optional[int] = SQLField(default=None, primary_key=True)

    # id of the user id , how
    value: Optional[str] = None
    ref: Optional[str] = SQLField(default=None, alias="$ref") # URI of the manager resource
    displayName: Optional[str] = None 

    user_id: Optional[int] = SQLField(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="manager")
    


class User(SQLModel, table = True):
    id: Optional[int] = SQLField(default = None, primary_key = True) 
    externalId: Optional[str] = None
    userName: str = SQLField(unique=True, index=True)
    displayName: Optional[str] = None
    active: Optional[bool] = True

    # Optional fields
    locale: Optional[str] = None
    timezone: Optional[str] = None
    nickName: Optional[str] = None
    profileUrl: Optional[str] = None
    title: Optional[str] = None
    userType: Optional[str] = None
    preferredLanguage: Optional[str] = None

   # required: Defines the schema URIs this resource uses
    schemas: list[str] = SQLField(default_factory=lambda: ["urn:ietf:params:scim:schemas:core:2.0:User"])

    # Parent side relationships
    name: Optional[Name] = Relationship(back_populates="user")
    emails: list[Email] = Relationship(back_populates="user")
    addresses: list[Address] = Relationship(back_populates="user")
    meta: Optional[Meta] = Relationship(back_populates="user")
    phoneNumbers: list[phoneNumber] = Relationship(back_populates="user")

    # enterprise
    employeeNumber: Optional[str] = None
    costCenter: Optional[str] = None
    organization: Optional[str] = None
    division: Optional[str] = None
    department: Optional[str] = None
    manager: Optional[Manager] = Relationship(back_populates="user")











