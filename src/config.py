import pathlib
import tomllib

from pydantic import BaseModel, HttpUrl, SecretStr

from enums import CountryCode

__all__ = (
    'CONFIG_FILE_PATH',
    'Config',
    'SentryConfig',
    'get_config',
)

CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / 'config.toml'


class SentryConfig(BaseModel):
    is_enabled: bool
    dsn: SecretStr
    traces_sample_rate: float
    profiles_sample_rate: float


class Config(BaseModel):
    auth_credentials_storage_base_url: HttpUrl
    units_storage_base_url: HttpUrl
    country_code: CountryCode
    sentry: SentryConfig


def get_config() -> Config:
    config = CONFIG_FILE_PATH.read_text(encoding='utf-8')
    config = tomllib.loads(config)
    return Config(
        auth_credentials_storage_base_url=(
            config['external_services_api']['auth_credentials_storage_base_url']
        ),
        units_storage_base_url=(
            config['external_services_api']['units_storage_base_url']
        ),
        country_code=config['country_code'],
        sentry=SentryConfig.model_validate(config['sentry']),
    )
