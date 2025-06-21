from typing import List, cast

from huggingface_hub import hf_hub_download
from llama_cpp import (
  ChatCompletionRequestSystemMessage,
  ChatCompletionRequestUserMessage,
  CreateChatCompletionResponse,
  Llama,
)

from model import Model
from utility import ConfigurationService, FileService, LoggingService

from .exception import (
  GenerationSourcesFileNotFoundError,
  GenerationSystemPromptFileNotFoundError,
  GenerationUserPromptFileEmptyError,
  GenerationUserPromptFileMissingTemplateError,
  GenerationUserPromptFileNotFoundError,
)


class GenerationService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @classmethod
  def run_inference(cls, models: List[Model], sources: List[str], system_prompt: str, user_prompt: str) -> None:
    LoggingService.mute_llamacpp_logging()
    LoggingService.error("NOT IMPLEMENTED YET.")

  @classmethod
  def run_chat_completion(cls, llm: Llama, system_prompt: str, user_prompt: str) -> str:
    system_message: ChatCompletionRequestSystemMessage = {"role": "system", "content": system_prompt}
    user_message: ChatCompletionRequestUserMessage = {"role": "user", "content": user_prompt}
    completion_response: CreateChatCompletionResponse = cast(CreateChatCompletionResponse, llm.create_chat_completion(
      messages=[system_message, user_message],
      max_tokens=1000,
    ))
    print(completion_response)
    answer = completion_response['choices'][0]['message']['content']
    return "" if answer is None else answer

  @classmethod
  def _load_model(cls, model: Model) -> Llama:
    # get model_path
    model_path = hf_hub_download(
      repo_id=model.repo_id,
      filename=model.gguf_filename,
      local_files_only=True
    )

    # load model into (V)RAM
    return Llama(
      model_path=model_path,
      n_gpu_layers=cls._get_gpu_layers(),
      verbose=False,
      n_ctx=512,
    )

  @classmethod
  def read_source_file(cls) -> List[str]:
    filename = cls._get_source_filepath()
    try:
      sources = FileService.from_csv_to_string_list(filename)
      LoggingService.info(f"In total {len(sources)} sentences were found in the sources.")
    except Exception as exc:
      raise GenerationSourcesFileNotFoundError(f"The sources file '{filename}' does not exist.") from exc
    return sources

  @classmethod
  def read_system_prompt(cls) -> str:
    filename = cls._get_system_prompt_filepath()
    try:
      system_prompt = FileService.from_file_to_string(filename)
      if system_prompt.strip() == "":
        LoggingService.info("No system prompt was configured")
      else:
        LoggingService.info(f"The configured system prompt is:\n{system_prompt}")
    except Exception as exc:
      raise GenerationSystemPromptFileNotFoundError(f"The system prompt file '{filename}' does not exist.") from exc
    return system_prompt

  @classmethod
  def read_user_prompt(cls) -> str:
    filename = cls._get_user_prompt_filepath()
    user_prompt_template_string = cls._get_user_prompt_template_string()
    try:
      user_prompt = FileService.from_file_to_string(filename)
      if user_prompt.strip() == "":
        raise GenerationUserPromptFileEmptyError(f"The user prompt file {filename} must not be empty") from None
      elif user_prompt_template_string not in user_prompt:
        raise GenerationUserPromptFileMissingTemplateError(f"The user prompt file {filename} needs to include {user_prompt_template_string}") from None
      else:
        LoggingService.info(f"The configured user prompt is:\n{user_prompt}")
    except Exception as exc:
      raise GenerationUserPromptFileNotFoundError(f"The user prompt file '{filename}' does not exist.") from exc
    return user_prompt

  @staticmethod
  def get_predictions_directory() -> str:
    return "predictions"

  @staticmethod
  def _get_gpu_layers() -> int:
    return 0 if ConfigurationService.get_environment_variable("USE_CPU") == "True" else -1

  @staticmethod
  def _get_source_filepath() -> str:
    return f"{ConfigurationService.get_data_directory()}/sources.csv"

  @staticmethod
  def _get_system_prompt_filepath() -> str:
    return f"{ConfigurationService.get_config_directory()}/system_prompt.txt"

  @staticmethod
  def _get_user_prompt_filepath() -> str:
    return f"{ConfigurationService.get_config_directory()}/user_prompt.txt"

  @staticmethod
  def _get_user_prompt_template_string() -> str:
    return "{source}"
