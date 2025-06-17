

from model import ModelCacheEmptyError, ModelCacheNotFoundError, ModelService
from utility import LoggingService


def clear_cache() -> None:
    try:
      delete_operation = ModelService.prepare_clear_model_cache()
    except (ModelCacheNotFoundError, ModelCacheEmptyError) as exc:
      LoggingService.info(str(exc))
      return
    except Exception as exc:
      LoggingService.error(str(exc))
      return
    if not LoggingService.confirm_action("Do you want to delete those models now?"):
        return
    try:
      ModelService.clear_model_cache(delete_operation)
    except Exception as exc:
      LoggingService.error(str(exc))
      return


if __name__ == "__main__":
    clear_cache()
