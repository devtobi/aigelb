
from model import ModelService
from utility import ConfigurationService, KeyboardInterruptError, LoggingService


def download_models():
  models = LoggingService.safe_exec_and_confirm(ModelService.read_model_list, "Are you sure you want to download those models?")
  if models is None:
    return

  try:
    ModelService.download_models(models)
  except KeyboardInterruptError as exc:
    LoggingService.info(str(exc))
    return

if __name__ == "__main__":
    ConfigurationService.load_environment_configuration()
    download_models()
