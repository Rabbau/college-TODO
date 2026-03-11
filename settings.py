from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='ignore'
    )

    DB_HOST: str = "localhost"
    DB_PORT: int = 5556
    DB_USER: str = "postgres"
    BD_DRIVER: str = "postgresql+psycopg2"
    DB_PASSWORD: str = "POSTGRES_PASSWORD"
    DB_NAME: str = "todo"
    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    NOTES_DIR: str = "notes"
    GOOGLE_CLIENT_ID: str = '779233572987-ho1tt82pf3s5d5h6b4qugdqqijjefp0b.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URL: str = 'http://localhost:8000/auth/google'
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    DEFAULT_CATEGORY_NAME: str = "Общее"
    DEFAULT_CATEGORY_TYPE: str = "default"

    @property
    def db_url(self):
        return f"{self.BD_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def google_redirect_url(self) -> str:
        return f"http://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URL}&scope=openid%20email&access_type=offline"
    
    @property
    def notes_path(self) -> Path:
        path = Path(self.NOTES_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
