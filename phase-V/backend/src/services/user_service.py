from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from ..models.user import User # Assuming User model is defined

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.exec(select(User).where(User.id == user_id)).first()

    def get_user_sort_preference(self, user_id: UUID) -> Optional[str]:
        """
        Retrieves a user's sort preference.
        """
        user = self.get_user_by_id(user_id)
        if user:
            return user.sort_preference
        return None

    def update_user_sort_preference(self, user_id: UUID, sort_preference: str) -> Optional[User]:
        """
        Updates a user's sort preference.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.sort_preference = sort_preference
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        return None

    # Other user-related methods (e.g., create, update, delete) would go here
