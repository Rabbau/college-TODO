from dataclasses import dataclass
import datetime as di
from datetime import timedelta
from jose import JWTError, jwt

from client import GoogleClient
from exception import TokenExpired, TokenNotCorrect, UserNotCorrectPasswordExpcection, UserNotFoundExpcection
from models.user import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from settings import Settings

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code=code)
        print(user_data)

    def get_google_redirect_url(self) -> str:
        return (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?response_type=code"
            f"&client_id={self.settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.settings.GOOGLE_REDIRECT_URL}"
            f"&scope=openid%20email%20profile"
            f"&access_type=offline"
            f"&prompt=consent"
        )

    def login(self, username:str, password:str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user=user,password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    @staticmethod
    def _validate_auth_user(user:UserProfile,password:str):
        if not user:
            raise UserNotFoundExpcection
        if user.password != password:
            raise UserNotCorrectPasswordExpcection

    def generate_access_token(self,user_id:int) -> str:
        expires_date_unix = (di.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expires_date_unix},
                            self.settings.JWT_SECRET_KEY, 
                            algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token
    
    def get_user_id_from_access_token(self, access_token:str)->int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        
        if payload['expire'] < di.datetime.utcnow().timestamp():
            raise TokenExpired
        
        return payload['user_id']
