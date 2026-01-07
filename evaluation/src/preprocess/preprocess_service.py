
from typing import Tuple

from requests import get

from utility import ConfigurationService, FileService, LoggingService

from .exception import DataDownloadError


class PreprocessService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @classmethod
  def read_download_url(cls) -> str:
    download_url = cls._get_download_url()
    if download_url == "":
      LoggingService.info(f"No download URL provided. Will try to read file from '{cls._get_data_filepath()}'.")
      return ""
    else:
      LoggingService.info(f"Configured download URL as: {download_url}")
    return download_url

  @classmethod
  def read_column_data(cls) -> Tuple[str, str, str]:
    source_column = cls._get_sources_column_name()
    reference_column = cls._get_references_column_name()
    column_separator = cls._get_column_separator()
    LoggingService.info(f"Configured source column name as: {source_column}")
    LoggingService.info(f"Configured reference column name as: {reference_column}")
    LoggingService.info(f"Configured column separator as: {column_separator}")
    return source_column, reference_column, column_separator

  @classmethod
  def get_data(cls, download_url: str, column_data: Tuple[str, str, str]) -> None:
    if download_url != "":
      cls._download_file(download_url)

    source_column_name = column_data[0]
    reference_column_name = column_data[1]
    column_separator = column_data[2]

    sources = FileService.from_csv(str, cls._get_data_filepath(), source_column_name, column_separator)
    references = FileService.from_csv(str, cls._get_data_filepath(), reference_column_name, column_separator)

    # Handle \n replacements
    replaced_sources = [s.replace("\\n", "\n") for s in sources]
    replaced_references = [s.replace("\\n", "\n") for s in references]

    FileService.to_csv(replaced_sources, cls.get_source_filepath(), simple_list=True)
    FileService.to_csv(replaced_references, cls.get_reference_filepath(), simple_list=True)
    LoggingService.info(f"Written sources and references to '{cls.get_source_filepath()}' and '{cls.get_reference_filepath()}'.")

  @classmethod
  def _download_file(cls, download_url) -> None:
    try:
      response = get(download_url)
      response.raise_for_status()

      save_path = cls._get_data_filepath()
      FileService.to_file_bytes(save_path, response.content)

      LoggingService.info(f"CSV file successfully downloaded and saved to: {save_path}")
    except Exception as exc:
      raise DataDownloadError(f"Error downloading the file from {download_url}") from exc

  @staticmethod
  def _get_download_url() -> str:
    download_url: str | None = ConfigurationService.get_environment_variable("DOWNLOAD_URL")
    return download_url if download_url is not None else ""

  @staticmethod
  def _get_sources_column_name() -> str:
    column_name: str | None = ConfigurationService.get_environment_variable("SOURCES_COLUMN_NAME")
    return column_name if column_name is not None else "source"

  @staticmethod
  def _get_references_column_name() -> str:
    column_name: str | None = ConfigurationService.get_environment_variable("REFERENCES_COLUMN_NAME")
    return column_name if column_name is not None else "reference"

  @staticmethod
  def _get_column_separator() -> str:
    column_separator: str | None = ConfigurationService.get_environment_variable("COLUMN_SEPARATOR")
    return column_separator if column_separator is not None else ","

  @staticmethod
  def _get_data_filepath() -> str:
    return f"{ConfigurationService.get_data_directory()}/data.csv"

  @staticmethod
  def get_source_filepath() -> str:
    return f"{ConfigurationService.get_data_directory()}/sources.csv"

  @staticmethod
  def get_reference_filepath() -> str:
    return f"{ConfigurationService.get_data_directory()}/references.csv"
