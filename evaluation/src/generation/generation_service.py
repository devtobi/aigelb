from typing import List, Optional, cast

from huggingface_hub import hf_hub_download
from llama_cpp import (
  ChatCompletionRequestResponseFormat,
  ChatCompletionRequestSystemMessage,
  ChatCompletionRequestUserMessage,
  CreateChatCompletionResponse,
  Llama,
)
from tqdm import tqdm

from model import Model, ModelService
from preprocess import PreprocessService
from utility import (
  ConfigurationService,
  DateService,
  FileService,
  KeyboardInterruptError,
  LoggingService,
)

from .exception import (
  GenerationModelInferenceError,
  GenerationModelLoadError,
  GenerationModelNotFoundError,
  GenerationPredictionWriteError,
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
    LoggingService.info("Running inference for models...")
    LoggingService.mute_llamacpp_logging()
    timestamp = cls._get_timestamp_from_lockfile()
    with tqdm(models) as pbar:
      for model in pbar:
        pbar.set_description(model.name)
        cls._run_inference_for_model(model, sources, system_prompt, user_prompt, timestamp)
    cls._remove_timestamp_file()
    LoggingService.info(f"Finished running inference for models. Written results to {cls._get_predictions_filepath(timestamp=timestamp)}")

  @classmethod
  def _run_inference_for_model(cls, model: Model, sources: List[str], system_prompt: str, user_prompt: str, timestamp: Optional[str] = None) -> None:
    llm = cls._load_model(model)
    predictions_filepath = cls._get_predictions_filepath(model, timestamp)
    sources_count = len(sources)
    if FileService.exists_file(predictions_filepath):
      count = FileService.count_csv_lines(predictions_filepath)
      if count == sources_count:
        return
      with tqdm(range(count, sources_count), desc="-> Running inference cycles", initial=count + 1, total=sources_count) as pbar:
        for i in pbar:
          u_prompt = user_prompt.replace(cls._get_user_prompt_template_string(), sources[i])
          result = cls._run_chat_completion(llm, model.name, system_prompt, u_prompt)
          cls._write_prediction(model, result, timestamp)
    else:
      with tqdm(sources, desc="-> Running inference cycles", leave=False) as pbar:
        for source in pbar:
          u_prompt = user_prompt.replace(cls._get_user_prompt_template_string(), source)
          result = cls._run_chat_completion(llm, model.name, system_prompt, u_prompt)
          cls._write_prediction(model, result, timestamp)

  @classmethod
  def _run_chat_completion(cls, llm: Llama, model_name: str, system_prompt: str, user_prompt: str) -> str:
    system_message: ChatCompletionRequestSystemMessage = {"role": "system", "content": system_prompt}
    user_message: ChatCompletionRequestUserMessage = {"role": "user", "content": user_prompt}
    try:
      completion_response: CreateChatCompletionResponse = cast(CreateChatCompletionResponse, llm.create_chat_completion(
        messages=[system_message, user_message],
        response_format=cls._get_response_format(),
        temperature=cls._get_temperature(),
      ))
    except KeyboardInterrupt:
        raise KeyboardInterruptError(f"The inference was interrupted by keyboard. Generation will be resumed on next run. Otherwise delete {cls._get_timestamp_filepath()} manually.") from None
    except Exception as exc:
      raise GenerationModelInferenceError(f"Failed running chat completion on '{model_name}'") from exc
    answer = completion_response['choices'][0]['message']['content']
    return "" if answer is None else answer

  @classmethod
  def _load_model(cls, model: Model) -> Llama:
    # get model_path
    try:
      model_path = hf_hub_download(
        repo_id=model.repo_id,
        filename=model.gguf_filename,
        local_files_only=True
      )
    except Exception as exc:
      raise GenerationModelNotFoundError(f"The model {model.name} could not be found") from exc

    # load model into (V)RAM
    try:
      return Llama(
        model_path=model_path,
        n_gpu_layers=cls._get_gpu_layers(),
        n_threads=cls._get_num_threads(),
        n_threads_batch=cls._get_num_threads(),
        n_ctx=cls._get_context_length(),
        verbose=False
      )
    except Exception as exc:
      raise GenerationModelLoadError(f"The model {model.name} could not be loaded") from exc

  @classmethod
  def _write_prediction(cls, model: Model, prediction: str, timestamp: Optional[str] = None) -> None:
    parsed_prediction = FileService.extract_value_from_json(prediction, cls._get_structured_output_key())
    filepath = cls._get_predictions_filepath(model, timestamp)
    try:
      FileService.append_to_csv(filepath, parsed_prediction)
    except Exception as exc:
      raise GenerationPredictionWriteError(f"Failed to write prediction to '{filepath}'") from exc

  @classmethod
  def read_source_file(cls) -> List[str]:
    filename = PreprocessService.get_source_filepath()
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

  @classmethod
  def _get_predictions_filepath(cls, model: Optional[Model] = None, timestamp: Optional[str] = None) -> str:
    model_filename = ModelService.get_filename(model) if model is not None else ""
    predictions_directory = cls.get_predictions_directory()
    timestamp_part = f"/{FileService.sanitize_file_name(timestamp)}" if timestamp is not None else ""
    return f"{predictions_directory}{timestamp_part}/{model_filename}.csv" if model_filename else f"{predictions_directory}{timestamp_part}/"

  @staticmethod
  def _get_system_prompt_filepath() -> str:
    return f"{ConfigurationService.get_config_directory()}/system_prompt.txt"

  @staticmethod
  def _get_user_prompt_filepath() -> str:
    return f"{ConfigurationService.get_config_directory()}/user_prompt.txt"

  @staticmethod
  def _get_user_prompt_template_string() -> str:
    return "{source}"

  @staticmethod
  def _get_timestamp_filename() -> str:
    return "timestamp.lock"

  @classmethod
  def _get_timestamp_filepath(cls) -> str:
    return f"{cls.get_predictions_directory()}/{cls._get_timestamp_filename()}"

  @classmethod
  def _get_timestamp_from_lockfile(cls) -> str:
    lockpath = cls._get_timestamp_filepath()
    if FileService.exists_file(lockpath):
      return FileService.from_file_to_string(lockpath)
    else:
      timestamp = DateService.get_timestamp()
      sanitized_timestamp = FileService.sanitize_file_name(timestamp)
      FileService.to_file(lockpath, sanitized_timestamp)
      return timestamp

  @classmethod
  def _remove_timestamp_file(cls) -> None:
    lockpath = cls._get_timestamp_filepath()
    FileService.delete_file(lockpath)

  @classmethod
  def _get_response_format(cls) -> ChatCompletionRequestResponseFormat:
    key = cls._get_structured_output_key()
    return {
      "type": "json_object",
      "schema": {
        "type": "object",
        "properties": { key: {"type": "string"} },
        "required": [key],
      },
    }

  @staticmethod
  def _get_gpu_layers() -> int:
    return 0 if ConfigurationService.get_environment_variable("USE_CPU") == "True" else -1

  @staticmethod
  def _get_structured_output_key() -> str:
    value = ConfigurationService.get_environment_variable("STRUCTURED_OUTPUT_KEY")
    return value if value is not None else "result"

  @staticmethod
  def _get_temperature() -> float:
    value = ConfigurationService.get_environment_variable("TEMPERATURE")
    return float(value) if value is not None else 0.2

  @staticmethod
  def _get_context_length() -> int:
    value = ConfigurationService.get_environment_variable("CONTEXT_LENGTH")
    return int(value) if value is not None else 0

  @staticmethod
  def _get_num_threads() -> Optional[int]:
    value = ConfigurationService.get_environment_variable("NUM_THREADS")
    return int(value) if value is not None else None
