from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ECKHO EMS API"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "eckho_ems"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()


