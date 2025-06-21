from typing import List

from generation import GenerationService
from model import Model, ModelService
from utility import ConfigurationService, KeyboardInterruptError, LoggingService


def run_inference():
  try:
    models: List[Model] = ModelService.read_model_list()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use those models for running inference?"):
    return
  try:
    sources: List[str] = GenerationService.read_source_file()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use those sentences for running inference?"):
    return
  try:
    system_prompt: str = GenerationService.read_system_prompt()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use this system prompt for running inference?"):
    return
  try:
    user_prompt: str = GenerationService.read_user_prompt()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use this user prompt for running inference?"):
    return
  try:
    GenerationService.run_inference(models, sources, system_prompt, user_prompt)
  except KeyboardInterruptError as exc:
    LoggingService.error(str(exc))
    return

if __name__ == "__main__":
    ConfigurationService.load_environment_configuration()
    run_inference()
