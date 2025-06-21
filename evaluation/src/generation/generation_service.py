from typing import List

from utility import FileService

from .exception import GenerationSourcesFileNotFoundError


class GenerationService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @staticmethod
  def get_predictions_directory() -> str:
    return "predictions"

  @classmethod
  def read_source_file(cls) -> List[str]:
    filename = cls._get_source_filename()
    try:
      return FileService.from_csv_to_string_list(filename)
    except Exception as exc:
      raise GenerationSourcesFileNotFoundError("Error reading sources from file") from exc

  @staticmethod
  def _get_source_filename() -> str:
    return "data/sources.csv"
