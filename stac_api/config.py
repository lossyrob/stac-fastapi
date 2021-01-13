"""Application settings."""
import enum
from typing import Optional, Set

from pydantic import BaseSettings


# TODO: Move to stac-pydantic
class ApiExtensions(enum.Enum):
    """
    Enumeration of available stac api extensions
    Ref: https://github.com/radiantearth/stac-api-spec/tree/master/extensions
    """

    context = "context"
    fields = "fields"
    query = "query"
    sort = "sort"
    transaction = "transaction"


class AddOns(enum.Enum):
    """
    Enumeration of available third party add ons
    """

    tiles = "tiles"


class ApiSettings(BaseSettings):
    """Application settings"""

    environment: str
    debug: bool = False

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = {"type"}

    # Fields which are item properties but indexed as distinct fields in the database model
    indexed_fields: Set[str] = {"datetime"}

    class Config:
        """model config"""

        extra = "allow"
        env_file = ".env"


settings: Optional[ApiSettings] = None


def inject_settings(base_settings: ApiSettings):
    """Inject settings to global scope"""
    global settings
    settings = base_settings
