from dataclasses import dataclass
from random import choice

from repository import UserRepository
from schema import UserLoginSchema
from service.auth import AuthService
from exception import UserAlreadyExistsException



@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username:str, password: str) -> UserLoginSchema:
        if self.user_repository.get_user_by_username(username=username):
            raise UserAlreadyExistsException
        user = self.user_repository.create_user(username=username, password=password)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
