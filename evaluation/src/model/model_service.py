from os import getenv
from typing import List

from pathvalidate import sanitize_filename

from utility import FileService, LoggingService

from .exception import ModelFileEmptyError, ModelFileNotFoundError
from .model import Model


class ModelService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @staticmethod
  def get_model_cache_dir() -> str:
    return getenv("HF_HOME") or "default HuggingFace cache directory (usually ~/.cache/huggingface)"

  @staticmethod
  def get_filename(model: Model) -> str:
    filename = (
      f"{model.repo_id}"
      + (f"__{model.gguf_filename}" if model.is_gguf else "")
    )
    return sanitize_filename(filename, replacement_text="_")

  @classmethod
  def read_model_list(cls) -> List[Model]:
    filename = cls._get_model_filename()
    try:
      models = FileService.from_csv(Model, filename)
      if len(models) == 0:
        raise ModelFileEmptyError(f"The model file {filename} contains no valid entries.") from None
      LoggingService.log_list(models, "The following models were given:")
      return models
    except Exception as exc:
      raise ModelFileNotFoundError(f"The model file '{filename}' does not exist.'") from exc

  @staticmethod
  def _get_model_filename() -> str:
    return "models.csv"
