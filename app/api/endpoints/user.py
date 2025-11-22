from fastapi import router
from fastapi import Depends

from sqlmodel import Session
from app.database import get_session

from app.services.user_service import UserService
from app.schemas.user_in import UserCreate
from app.schemas.user_out import UserPublic
 
@router.post("/Users", response_model=UserPublic, status_code=201)
def create_user(user_in: UserCreate, session:Session = Depends(get_session)):
    service = UserService(session)
    db_user = service.create_user(user_in)
    return UserPublic.model_validate(db_user)

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
             