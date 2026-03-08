from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from dataclasses import dataclass
from sqlalchemy.orm import Session
from  models import UserProfile
from exception import UserAlreadyExistsException

@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, username:str,password:str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username, 
            password=password
        ).returning(UserProfile.id)
        with self.db_session() as session:
            try:
                user_id: int = session.execute(query).scalar()
                session.commit()
                session.flush()
                return self.get_user(user_id)
            except IntegrityError:
                session.rollback()
                raise UserAlreadyExistsException
        
    
    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            user: UserProfile = session.execute(query).scalar_one_or_none()
        return user
    
    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            return session.execute(query).scalars().first()
