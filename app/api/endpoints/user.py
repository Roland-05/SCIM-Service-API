from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas.sub_schemas import ManagerScim, MetaScim, EnterpriseExtensionScim

from sqlmodel import Session
from app.database import get_session

from app.services.user_service import UserService
from app.schemas.user_in import UserCreate
from app.schemas.user_out import UserPublic
from app.schemas.user_update import UserUpdate

router = APIRouter()
 
@router.post("/Users", response_model=UserPublic, status_code=201)
def create_user(user_in: UserCreate, session:Session = Depends(get_session)):
    service = UserService(session)
    db_user = service.create_user(user_in)
    return to_scim_user(db_user)

@router.get("/Users/{userid}", response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    service = UserService(session)
    user = service.get_user(user_id)
    return UserPublic.model_validate(user)

@router.get("/Users", response_model=list[UserPublic])
def list_users(session: Session = Depends(get_session)):
    service = UserService(session)
    users = service.list_users()
    return [UserPublic.model_validate(u) for u in users]

@router.get("/Users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session:Session = Depends(get_session)):

    service = UserService(session)
    updated = service.update_user(user_id, user_update)

    return to_scim_user(updated)

def to_scim_user(db_user):

    """
    Convert a SQLModel User ORM object into a SCIM-compliant UserPublic response model.

    This helper performs all SCIM-specific response shaping:
    - Converts ORM attributes → Pydantic (UserPublic) model
    - Dynamically generates the SCIM `meta` block (not stored in DB)
    - Formats manager relationship in SCIM format
    - Prepares the final JSON-ready response object
    
    This function is intentionally kept outside the service layer because
    meta attributes are *API-layer concerns* (not persisted in the database).
    """

    public = UserPublic.model_validate(db_user)
    
    public.meta = MetaScim(
        resource_type="User",
        created=db_user.created,     # if you have it
        last_modified=datetime.utcnow(),
        location=f"/Users/{db_user.id}",
        version=None
    )

    # manager mapping
    if db_user.manager:
        public.manager = ManagerScim(manager_user_id=str(db_user.manager.manager_user_id),
                                     manager_ref=f"/Users/{db_user.manager.manager_user_id}",
                                     display_name=db_user.manager.display_name)
        
    
    public.enterprise_extension = EnterpriseExtensionScim(
        employee_number=db_user.employee_number,
        department=db_user.department,
        cost_center=db_user.cost_center)

    return public