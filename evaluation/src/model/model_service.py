from os import getenv
from typing import List

from huggingface_hub import (
  CacheNotFound,
  DeleteCacheStrategy,
  HFCacheInfo,
  hf_hub_download,
  scan_cache_dir,
)

from utility import (
  ConfigurationService,
  FileService,
  KeyboardInterruptError,
  LoggingService,
)

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
  def get_filename(model: Model) -> str:
    return FileService.sanitize_file_name(model.name)

  @classmethod
  def read_model_list(cls) -> List[Model]:
    filename = cls._get_model_filepath()
    try:
      models = FileService.from_csv(Model, filename)
      if len(models) == 0:
        raise ModelFileEmptyError(f"The model file {filename} contains no valid entries.") from None
      LoggingService.log_list(models, "The following models were configured:")
      return models
    except Exception as exc:
      raise ModelFileNotFoundError(f"The model file '{filename}' does not exist.'") from exc

  @classmethod
  def download_models(cls, models: List[Model]) -> None:
    LoggingService.info(f"Downloading models from Hugging Face to '{cls._get_model_cache_dir()}'...")
    for model in models:
      cls._download_model(model)
    LoggingService.info("Finished downloading the models from Hugging Face.")

  @staticmethod
  def prepare_clear_model_cache() -> DeleteCacheStrategy:
    # Read local cache
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
    try:
      strategy.execute()
      LoggingService.info("Successfully cleared the cache.")
    except Exception as exc:
      raise ModelCacheClearError("Failed to clear the model cache.") from exc

  @classmethod
  def _download_model(cls, model: Model) -> None:
    if model.repo_id is None or model.repo_id == "":
      LoggingService.error("Failed to download a model because the repo_id is empty.")
    try:
      cls._download_gguf_model(model)
    except ModelDownloadError as exc:
      if model.gated:
        LoggingService.error(f'Failed downloading gated model "{model}".'
          f' Please confirm you added a valid Hugging Face access token'
          f' and are granted access to the model files.')
      else:
        LoggingService.error(str(exc))

  @staticmethod
  def _download_gguf_model(model: Model) -> None:
    if model.gguf_filename is None or model.gguf_filename == "":
      raise ModelDownloadError(f"The gguf_filename of {model.repo_id} cannot be empty.")
    try:
      hf_hub_download(
        repo_id=model.repo_id,
        filename=model.gguf_filename,
        repo_type="model",
        token=model.gated,
      )
    except KeyboardInterrupt:
      raise KeyboardInterruptError("The download of the model was interrupted by keyboard. Proceeding on next run.") from None
    except Exception as exc:
      raise ModelDownloadError(f"Failed to download GGUF model '{model.name}'") from exc

  @staticmethod
  def _get_model_filepath() -> str:
    return f"{ConfigurationService.get_config_directory()}/models.csv"

  @staticmethod
  def _get_model_cache_dir() -> str:
    return getenv("HF_HOME") or "default HuggingFace cache directory (usually ~/.cache/huggingface)"
