from logging import Logger
from typing import List

from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

from utility import (
    Model,
    confirm_action,
    from_csv,
    get_logger,
    get_model_cache_dir,
    log_list,
)


def download(downloadable_models: List[Model], logger: Logger) -> bool:
    logger.info(f"Downloading models from Hugging Face to '{get_model_cache_dir()}'...")
    for model in downloadable_models:
        try:
            if model.is_gguf:
                # Download GGUF model
                logger.info(f"Downloading '{model.repo_id}/{model.gguf_filename}'...")
                hf_hub_download(
                    repo_id=model.repo_id,
                    filename=model.gguf_filename,
                    repo_type="model",
                    token=model.gated,
                )
            else:
                # Download standard transformers-based model
                logger.info(f"Downloading required files for '{model.repo_id}'...")
                AutoTokenizer.from_pretrained(model.repo_id)
                AutoModelForCausalLM.from_pretrained(model.repo_id)
        except OSError:
            if model.gated:
                logger.warning(
                    f'Failed downloading gated model "{model}".'
                    f" Please confirm you added a valid Hugging Face access token"
                    f" and are granted access to the model files."
                )
            else:
                logger.warning(
                    f'Failed downloading model "{model}".'
                    f" Please check the entry in models.csv is correct."
                )
        except KeyboardInterrupt:
            logger.warning(
                "Interrupted download. Proceeding on next execution. Quitting..."
            )
            return False
    logger.info("Finished downloading the models from Hugging Face. Quitting...")
    return True

def download_models(logger: Logger):
    logging.set_verbosity_error()
    models: List[Model] = from_csv(Model, "models.csv")
    if len(models) == 0:
      logger.info("No models in models.csv. Please add some models first and re-run this script.")
      return
    log_list(models, logger, "The following models were requested:")

    if not confirm_action(logger, "Are you sure you want to download those models?"):
        return
    if not download(models, logger):
        return

if __name__ == "__main__":
    # Load env variable for optional API authentication
    log: Logger = get_logger()
    load_dotenv()

    download_models(log)
