from pydantic import BaseSettings


class Settings(BaseSettings):
    sql_url: str
    secret_key: str
    algorithm: str
    access_token_expire_time: int

    class Config:
        env_file = ".env"


setting = Settings()
