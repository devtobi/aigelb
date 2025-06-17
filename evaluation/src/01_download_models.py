from typing import List

from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

from utility import (
    FileService,
    LoggingService,
)

from model import (
    Model,
    ModelService
)


def download(downloadable_models: List[Model]) -> bool:
    LoggingService.info(f"Downloading models from Hugging Face to '{ModelService.get_model_cache_dir()}'...")
    for model in downloadable_models:
        try:
            if model.is_gguf:
                # Download GGUF model
                LoggingService.info(f"Downloading '{model.repo_id}/{model.gguf_filename}'...")
                hf_hub_download(
                    repo_id=model.repo_id,
                    filename=model.gguf_filename,
                    repo_type="model",
                    token=model.gated,
                )
            else:
                # Download standard transformers-based model
                LoggingService.info(f"Downloading required files for '{model.repo_id}'...")
                AutoTokenizer.from_pretrained(model.repo_id)
                AutoModelForCausalLM.from_pretrained(model.repo_id)
        except OSError:
            if model.gated:
                LoggingService.warn(
                    f'Failed downloading gated model "{model}".'
                    f" Please confirm you added a valid Hugging Face access token"
                    f" and are granted access to the model files."
                )
            else:
                LoggingService.warn(
                    f'Failed downloading model "{model}".'
                    f" Please check the entry in models.csv is correct."
                )
        except KeyboardInterrupt:
            LoggingService.warn(
                "Interrupted download. Proceeding on next execution. Quitting..."
            )
            return False
    LoggingService.info("Finished downloading the models from Hugging Face. Quitting...")
    return True

def download_models():
    logging.set_verbosity_error()
    models: List[Model] = FileService.from_csv(Model, "models.csv")
    if len(models) == 0:
      LoggingService.info("No models in models.csv. Please add some models first and re-run this script.")
      return
    LoggingService.log_list(models, "The following models were requested:")

    if not LoggingService.confirm_action("Are you sure you want to download those models?"):
        return
    if not download(models):
        return

if __name__ == "__main__":
    # Load env variable for optional API authentication
    load_dotenv()

    download_models()
