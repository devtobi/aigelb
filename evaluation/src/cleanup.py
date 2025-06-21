

from model import ModelCacheEmptyError, ModelCacheNotFoundError, ModelService
from utility import LoggingService


def clear_cache() -> None:
  delete_operation = LoggingService.safe_exec_and_confirm(ModelService.prepare_clear_model_cache, "Do you want to delete those models now?")
  if delete_operation is None:
    return

  try:
    ModelService.clear_model_cache(delete_operation)
  except Exception as exc:
    LoggingService.error(str(exc))
    return


if __name__ == "__main__":
    clear_cache()
