from generation import GenerationService
from model import ModelService
from utility import ConfigurationService, KeyboardInterruptError, LoggingService


def run_inference():
  models = LoggingService.safe_exec_and_confirm(ModelService.read_model_list, "Are you sure you want to use those models for running inference?")
  if models is None:
    return

  sources = LoggingService.safe_exec_and_confirm(GenerationService.read_source_file, "Are you sure you want to use those sentences for running inference?")
  if sources is None:
    return

  system_prompt = LoggingService.safe_exec_and_confirm(GenerationService.read_system_prompt, "Are you sure you want to use this system prompt for running inference?")
  if system_prompt is None:
    return

  user_prompt = LoggingService.safe_exec_and_confirm(GenerationService.read_user_prompt, "Are you sure you want to use this user prompt for running inference?")
  if user_prompt is None:
    return

  try:
    GenerationService.run_inference(models, sources, system_prompt, user_prompt)
  except KeyboardInterruptError as exc:
    LoggingService.error(str(exc))
    return

if __name__ == "__main__":
    ConfigurationService.load_environment_configuration()
    run_inference()
