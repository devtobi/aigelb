from os import getenv
from typing import List

from huggingface_hub import (
  CacheNotFound,
  DeleteCacheStrategy,
  HFCacheInfo,
  hf_hub_download,
  scan_cache_dir,
)
from transformers import AutoModelForCausalLM, AutoTokenizer

from utility import FileService, KeyboardInterruptError, LoggingService

from .exception import (
  ModelCacheClearError,
  ModelCacheEmptyError,
  ModelCacheNotFoundError,
  ModelDownloadError,
  ModelFileEmptyError,
  ModelFileNotFoundError,
)
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
    return FileService.sanitize_file_name(filename)

  @classmethod
  def read_model_list(cls) -> List[Model]:
    filename = cls._get_model_filename()
    LoggingService.info(f"Reading models from {filename}...")
    try:
      models = FileService.from_csv(Model, filename)
      if len(models) == 0:
        raise ModelFileEmptyError(f"The model file {filename} contains no valid entries.") from None
      LoggingService.log_list(models, "The following models were found:")
      return models
    except Exception as exc:
      raise ModelFileNotFoundError(f"The model file '{filename}' does not exist.'") from exc

  @classmethod
  def download_models(cls, models: List[Model]) -> None:
    LoggingService.info(f"Downloading models from Hugging Face to '{cls.get_model_cache_dir()}'...")
    for model in models:
      cls._download_model(model)
    LoggingService.info("Finished downloading the models from Hugging Face.")

  @staticmethod
  def prepare_clear_model_cache() -> DeleteCacheStrategy:
    # Read local cache
    LoggingService.info("Collecting model information from cache...")
    try:
      huggingface_cache_info: HFCacheInfo = scan_cache_dir()
    except CacheNotFound as exc:
      raise ModelCacheNotFoundError("The cache directory does not exist, thus nothing needs to be cleared.") from exc

    # Extract revision commit hashes
    revisions: List[str] = [
      revision.commit_hash
      for repo in huggingface_cache_info.repos
      for revision in repo.revisions
    ]
    if not revisions:
      raise ModelCacheEmptyError("Cache directory found, but no models were downloaded yet.")

    delete_operation: DeleteCacheStrategy = huggingface_cache_info.delete_revisions(*revisions)
    LoggingService.info(
      f"Found {len(revisions)} models in cache."
      f" Freeing will re-claim {delete_operation.expected_freed_size_str}B"
    )
    return delete_operation

  @staticmethod
  def clear_model_cache(strategy: DeleteCacheStrategy) -> None:
    LoggingService.info("Clearing model information from cache...")
    try:
      strategy.execute()
      LoggingService.info("Successfully cleared the cache.")
    except Exception as exc:
      raise ModelCacheClearError("Failed to clear the model cache.") from exc

  @classmethod
  def _download_model(cls, model: Model) -> None:
    try:
      if model.is_gguf:
        cls._download_gguf_model(model.repo_id, model.gguf_filename, model.gated)
      else:
        cls._download_transformers_model(model.repo_id)
    except ModelDownloadError as exc:
      if model.gated:
        LoggingService.error(f'Failed downloading gated model "{model}".'
          f' Please confirm you added a valid Hugging Face access token'
          f' and are granted access to the model files.')
      else:
        LoggingService.error(str(exc))

  @staticmethod
  def _download_transformers_model(repo_id: str) -> None:
    LoggingService.info(f"Downloading required files for '{repo_id}'...")
    try:
      AutoTokenizer.from_pretrained(repo_id)
      AutoModelForCausalLM.from_pretrained(repo_id)
    except KeyboardInterrupt:
      raise KeyboardInterruptError("The download of the model was interrupted by keyboard. Proceeding on next run.") from None
    except Exception as exc:
      raise ModelDownloadError(f"Failed to download transformers model '{repo_id}'") from exc

  @staticmethod
  def _download_gguf_model(repo_id: str, gguf_filename: str, gated: bool) -> None:
    LoggingService.info(f"Downloading '{repo_id}/{gguf_filename}'...")
    try:
      hf_hub_download(
        repo_id=repo_id,
        filename=gguf_filename,
        repo_type="model",
        token=gated,
      )
    except KeyboardInterrupt:
      raise KeyboardInterruptError("The download of the model was interrupted by keyboard. Proceeding on next run.") from None
    except Exception as exc:
      raise ModelDownloadError(f"Failed to download GGUF model '{gguf_filename}'") from exc

  @staticmethod
  def _get_model_filename() -> str:
    return "models.csv"
