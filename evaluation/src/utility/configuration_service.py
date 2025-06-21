from os import getenv
from typing import Optional

from dotenv import load_dotenv

from .file_service import FileService


class ConfigurationService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @staticmethod
  def get_data_directory() -> str:
    return "data"

  @staticmethod
  def get_config_directory() -> str:
    return "config"

  @staticmethod
  def get_environment_variable(name: str) -> Optional[str]:
    return getenv(name)

  @classmethod
  def load_environment_configuration(cls) -> None:
    path = FileService.get_absolute_path(ConfigurationService.get_config_directory())
    filepath = f"{path}/{cls._get_environment_filename()}"
    load_dotenv(filepath)

  @staticmethod
  def _get_environment_filename() -> str:
    return "config.env"
