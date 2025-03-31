from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

from helper import confirm_action, get_logger, get_model_cache_dir, get_models


def log_models(models, logger):
    for mdl in models:
        logger.info(f"| {mdl}")

def log_requested_models(requested_models, logger):
    logger.info("The following models were requested:")
    log_models(requested_models, logger)

def download(downloadable_models, model_cache_dir, logger):
    logger.info("Downloading models from Hugging Face...")
    for model in downloadable_models:
        gated = model.gated == "True"
        try:
            if model.gguf_filename.strip():
                # Download GGUF model
                logger.info(f"Downloading '{model.repo_id}/{model.gguf_filename}'...")
                hf_hub_download(
                    repo_id=model.repo_id,
                    filename=model.gguf_filename,
                    repo_type="model",
                    cache_dir=model_cache_dir,
                    token=gated,
                )
            else:
                # Download standard transformers-based model
                logger.info(f"Downloading required files for '{model.repo_id}'...")
                AutoTokenizer.from_pretrained(model.repo_id, cache_dir=model_cache_dir)
                AutoModelForCausalLM.from_pretrained(
                    model.repo_id, cache_dir=model_cache_dir
                )
        except OSError:
            if gated:
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

def download_models(logger):
    logging.set_verbosity_error()

    models = get_models()
    log_requested_models(models, logger)

    if not confirm_action(logger, "Are you sure you want to download those models?"):
        return

    model_cache_dir = get_model_cache_dir()
    if not download(models, model_cache_dir, logger):
        return

if __name__ == "__main__":
    # Load env variable for optional API authentication
    log = get_logger()
    load_dotenv()

    download_models(log)
