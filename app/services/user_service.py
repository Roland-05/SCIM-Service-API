from sqlmodel import Session, select # select builds sql query
from app.models.user import User
from app.schemas.user_in import UserCreate # input schema
from app.models.user import Name, Email, Meta, Manager, Address, Role, PhoneNumber, EnterpriseExtension, Manager
from app.schemas.user_update import UserUpdate
from fastapi import HTTPException




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
            setattr(db_user, field, value)

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)



        return db_user