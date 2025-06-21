from typing import List

from dotenv import load_dotenv

from model import Model, ModelService
from utility import KeyboardInterruptError, LoggingService


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
    # Load env variable for optional API authentication
    load_dotenv()

    download_models()
