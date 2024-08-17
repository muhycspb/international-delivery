
from dynaconf import Dynaconf

_settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
)


class Settings:
    postgres_host = _settings.postgres.host
    postgres_port = _settings.postgres.port
    postgres_database = _settings.postgres.db
    postgres_username = _settings.postgres.user
    postgres_password = _settings.postgres.password

    redis_container_name = _settings.redis.container_name


settings = Settings()
