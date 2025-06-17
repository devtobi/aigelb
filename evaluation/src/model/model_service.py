from os import getenv

from pathvalidate import sanitize_filename

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
