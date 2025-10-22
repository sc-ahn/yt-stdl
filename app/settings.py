from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SRCDIR = Path(__file__).parent.parent.resolve()
ROOTDIR = SRCDIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SRCDIR / ".env",
        env_prefix="YTSTDL_",
        extra="ignore",
        env_file_encoding="utf-8",
    )
    API_KEY: str = ""
    WEBSHARE_USERNAME: str = ""
    WEBSHARE_PASSWORD: str = ""
    ENABLE_PROXY: bool = False


EXAMPLE_DIR = Path(__file__).resolve().parent.parent / "example"
print(EXAMPLE_DIR)


@lru_cache
def get_settings() -> Settings:
    return Settings()


env = get_settings()
