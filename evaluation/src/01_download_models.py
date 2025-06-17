from typing import List

from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer

from model import Model, ModelService
from utility.logging_service import (
    LoggingService,
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
                LoggingService.error(
                    f'Failed downloading gated model "{model}".'
                    f" Please confirm you added a valid Hugging Face access token"
                    f" and are granted access to the model files."
                )
            else:
                LoggingService.error(
                    f'Failed downloading model "{model}".'
                    f" Please check the entry in models.csv is correct."
                )
        except KeyboardInterrupt:
            LoggingService.info(
                "Interrupted download. Proceeding on next execution. Quitting..."
            )
            return False
    LoggingService.info("Finished downloading the models from Hugging Face. Quitting...")
    return True

def download_models():
    LoggingService.mute_transformers_logging()
    try:
      models: List[Model] = ModelService.read_model_list()
    except Exception as msg:
      LoggingService.error(str(msg))
      return

    if not LoggingService.confirm_action("Are you sure you want to download those models?"):
        return
    if not download(models):
        return

if __name__ == "__main__":
    # Load env variable for optional API authentication
    load_dotenv()

    download_models()
