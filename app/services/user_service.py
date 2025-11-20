from sqlmodel import Session
from app.models.user import User
from app.schemas.user_in import UserCreate # input schema
from app.models.user import Name, Email, Meta, Manager, Address, PhoneNumber

from datetime import datetime

class UserService: 
    """ Handles all business logic and persistence for the User resource. """

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserCreate) -> User:

        """
        Converts the pydantic input schema in to a database model,
        handles nested objects, and persists the new user.
        """