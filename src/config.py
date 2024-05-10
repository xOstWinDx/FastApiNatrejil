from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET: str

    SMTP_USER: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    DB_HOST_TEST: str = "None"
    DB_PORT_TEST: int = 0
    DB_USER_TEST: str = "None"
    DB_PASS_TEST: str = "None"
    DB_NAME_TEST: str = "None"

    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_TEST(self):
        return f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'

    model_config = SettingsConfigDict(env_file=('.env-non-dev'), extra='ignore')


settings = Settings()
