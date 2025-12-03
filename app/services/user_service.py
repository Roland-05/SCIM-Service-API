from sqlmodel import Session, select # select builds sql query
from app.models.user import User
from app.schemas.user_in import UserCreate # input schema
from app.models.user import Name, Email, Meta, Manager, Address, Role, PhoneNumber, EnterpriseExtension, Manager
from app.schemas.user_update import UserUpdate
from app.schemas.user_patch import UserPatch, PatchRequest
from fastapi import HTTPException
from typing import Any
from pydantic.alias_generators import to_snake
import re


ENTERPRISE_FIELDS = [
    "employee_number", 
    "cost_center", 
    "organization", 
    "division", 
    "department"
]


class UserService: 
    """ Handles all business logic and persistence for the User resource. """

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserCreate) -> User:

        """
        Converts the pydantic input schema in to a database model,
        handles nested objects, and persists the new user.
        Read and write to database.
        """

        # dump data (json) from the api object
        user_data = user_in.model_dump(exclude_unset=True)

        # flatten the complex types as database cannot  handle nested types 
        name_data = user_data.pop("name", None)
        emails_data = user_data.pop("emails", None)
        addresses_data = user_data.pop("addresses", None)
        manager_data = user_data.pop("manager", None)
        roles_data = user_data.pop("roles", None) 
        phone_number_data = user_data.pop("phone_numbers", None)
        enterprise_data = user_data.pop("enterprise_extension", None)

        # split core vs enterprise fields
        core_data = {}
        enterprise_data = {}

        for key, value in user_data.items():
            if key in ENTERPRISE_FIELDS:
                enterprise_data[key] = value
            else:
                core_data[key] = value

        # build main user model from core data
        db_user = User.model_validate(core_data)

        # attach relationships
        if name_data: 
            db_user.name = Name.model_validate(name_data)
        
        if emails_data: 
            db_user.emails = [Email.model_validate(e) for e in emails_data]

        if addresses_data: 
            db_user.addresses = [Address.model_validate(a) for a in addresses_data]

        if manager_data: 
            db_user.manager = Manager.model_validate(manager_data)
        
        if roles_data:
            db_user.roles = [Role.model_validate(r) for r in roles_data]

        if phone_number_data:
            db_user.phone_numbers = [PhoneNumber.model_validate(p) for p in phone_number_data]
        
        if db_user.manager and db_user.manager.manager_user_id:
            db_user.manager = Manager.model_validate(manager_data)

        if enterprise_data: 
            db_user.enterprise_extension = EnterpriseExtension.model_validate(enterprise_data)


 

        # commit
        self.session.add(db_user)  
        self.session.commit()
        self.session.refresh(db_user)

        return db_user  
        
    
    def get_user(self, user_id:int):
        user = self.session.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    def list_users(self):
        return self.session.exec(select(User)).all()
    


    def update_user(self, user_id: int, data: UserUpdate):
        db_user = self.get_user(user_id)

        
        update_data = data.model_dump(exclude_unset=True)

        for field,value in update_data.items():
            setattr(db_user, field, value) # update the values

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)



        return db_user
    
    def patch_user(self, user_id: int, patch: PatchRequest):

        db_user = self.get_user(user_id)
        op_type = op.op
        for op in patch.Operations:
            if op_type.lower() == "replace":
                self._apply_replace(db_user, op.path, op.value)
            elif op_type == "add":
                _apply_add(db_user, op.path, op.value)
            
            elif op_type == "remove":
                # TODO: implement remove later
                raise NotImplementedError("remove not implemented yet")

            else:
                raise NotImplementedError(f"Unsupported PATCH op: {op.op}")
            
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def _apply_replace(self, resource, path:str, value: Any):
        """
        Apply a SCIM 'replace' operation.
        Supports:
        - simple attributes (displayName)
        - nested attributes (name.givenName)
        - full multi-valued replacement (emails)
        - filtered list replacement (emails[type eq "work"])

        """

        if not path: 
            raise NotImplementedError("Patch without path")
        

        attributes = path.split('.')

        head = attributes[0]
        tail = attributes[1:]
        


        # parse attribute + optional filter
        attr_name, flt = _parse_attribute_filter(head)
        
        attr_name = to_snake(attr_name)

        # handle simple attribute with no filter and no ntesting
        if not flt and not tail:
            setattr(resource, attr_name, value)
            return

        # get the base attribute (list or object)
        target = getattr(resource, attr_name, None)
        if target is None:
            raise ValueError(f"Attribute '{attr_name}' not present on resource.")

        if flt:
            _apply_replace_filtered_list(resource, attr_name, target, flt, tail, value)

        # case 2: no filter but nested > nested object
        for part in attributes[:-1]:
            target = getattr(target, part)
                        
        leaf = attributes[-1]

        setattr(target, leaf, value)


# patch add
# if path is multi-valued append new items
# if path is attribute set attribute
# if attribute missing, create it

def _parse_attribute_filter(s: str):
    """
    Extract attribute name and filter expression from e.g.:
      emails[type eq "work"]
    Returns:
      ("emails", ('type', 'eq', 'work'))
    or:
      ("emails", None)
    """

    # No filter present
    if "[" not in s:
        return s, None

    attr = s[:s.index("[")]
    #extract filter
    inside = s[s.index("[")+1 : s.rindex("]")]

    # Basic SCIM filter: attr op "value"
    m = re.match(r'(\w+)\s+(eq)\s+"([^"]+)"', inside.strip())
    if not m:
        raise ValueError(f"Unsupported filter: {inside}")

    return attr, (m.group(1), m.group(2), m.group(3))


def _apply_replace_filtered_list(resource, attr_name, target_list, flt, tail, value):
    """
    Handles paths like:
      emails[type eq "work"].value = "new@example.com"
    """
    filter_attr, _, filter_val = flt

    #convert camelCase to snake_case for filter attribute
    filter_attr = to_snake(filter_attr)

    # Find matching items in the list
    matches = [
        item for item in target_list
        if getattr(item, filter_attr, None) == filter_val
    ]

    if not matches:
        raise ValueError(
            f"No items in '{attr_name}' match filter {filter_attr} == {filter_val}"
        )

    # If tail is empty, replace entire element(s)
    if not tail:
        for i, item in enumerate(target_list):
            if getattr(item, filter_attr, None) == filter_val:
                target_list[i] = value
        return

    # Otherwise apply nested replace inside each matched object
    leaf = to_snake(tail[-1])

    for item in matches:
        setattr(item, leaf, value)



# Patch Add. add inside filtered multi-valued attributes to be done later

def _apply_add(resource, path:str, value):

    """
    Patch Add

    Supports: 
    - add/assign to simple attributes (e.g. displayName)
    - append/extend multi-valued attributes (e.g. "emails")
    - nested attributes

    """

    if not path: 
        if not isinstance(value, dict):
            raise ValueError("PATCH add without path must have object 'value'")
        
    
        for key, v in value.items():
            attr_name = to_snake(key)
            current = getattr(resource, attr_name, None)

            if current is None:
                # if no attribute, set it
                setattr(resource, attr_name, v)

            # if the value is a list
            elif isinstance(current, list):
                # extend the list from the list
                if isinstance(v, list):
                    current.extend(v)
                else:
                    # append element to the list
                    current.append(v)
            else:
                setattr(resource, attr_name, v)
        return

    # no path
    parts = path.split(".")
    head = parts[0]
    tail = parts[1:]

    attr_name, flt = _parse_attribute_filter(head)
    attr_name = to_snake(attr_name)

    target = getattr(resource, attr_name, None)

    if target is None:
        if tail:
            # add into a nested attribute that doesn't exist
            # treat like error for now
            raise ValueError(f"Cannot add into missing nested attribute: {path}")
        
        else:
            setattr(resource, attr_name, value)
            return

        
        

    # filter
    if flt:
        raise NotImplementedError("add with filtered list target not implemented yet")
    
    # no filter but target is a list, append/extend

    if isinstance(target, list):
        if isinstance(value, list):
            target.extend(value)
        else:
            target.append(value)

    
    # no filter, nested path(e.g. name.givenName)

    current = target
    for part in parts[1:-1]:
        current=getattr(current, to_snake(part))

    leaf = to_snake(parts[-1])

    existing_leaf_val = getattr(current, leaf, None)

    if isinstance(existing_leaf_val, list):
        if isinstance(value, list):
            existing_leaf_val.extend(value)
        else:
            existing_leaf_val.append(value)
        
    else:
        setattr(current, leaf, value)