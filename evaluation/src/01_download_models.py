from typing import List

from model import Model, ModelService
from utility import ConfigurationService, KeyboardInterruptError, LoggingService


def download_models():
    try:
      models: List[Model] = ModelService.read_model_list()
    except Exception as exc:
      LoggingService.error(str(exc))
      return
    if not LoggingService.confirm_action("Are you sure you want to download those models?"):
        return
    try:
      ModelService.download_models(models)
    except KeyboardInterruptError as exc:
      LoggingService.error(str(exc))
      return

if __name__ == "__main__":
    ConfigurationService.load_environment_configuration()
    download_models()
