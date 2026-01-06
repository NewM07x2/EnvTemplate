from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/postgres"
    SUPABASE_URL: str = "http://postgres:5432"
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = "super-secret-jwt-token-with-at-least-32-characters-long"
    
    class Config:
        env_file = ".env"

settings = Settings()
