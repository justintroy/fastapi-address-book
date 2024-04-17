from pydantic_settings import BaseSettings

# Centralized config with Pydantic
# This gives the ability to import this class
# and use it whenever needed, with extra validation
# and type-hints.

class Config(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///database.db" # Default value if not available
    AUTH_SECRET_KEY: str = "s3cr3t"

# will read from .env file if available
config = Config(_env_file='.env', _env_file_encoding='utf-8')