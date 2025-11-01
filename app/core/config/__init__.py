import os

from app.core.config.base import BaseConfig
from app.core.config.development import DevelopmentConfig


def get_current_config() -> type[BaseConfig]:
    """Get the current configuration based on the ENVIRONMENT variable.

    Returns:
        Configuration class based on the current environment.
        Defaults to DevelopmentConfig if ENVIRONMENT is not set.
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()

    config_mapping = {
        "development": DevelopmentConfig,
    }

    config_class = config_mapping.get(environment, DevelopmentConfig)
    return config_class
