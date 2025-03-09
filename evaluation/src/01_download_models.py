from dotenv import load_dotenv
from huggingface_hub import hf_hub_download, scan_cache_dir, try_to_load_from_cache
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

from helper import confirm_action, get_logger, get_model_cache_dir, get_models


def get_cached_models(models, model_cache_dir):
    huggingface_cache_info = scan_cache_dir(cache_dir=model_cache_dir)
    cached_repo_names = [repo.repo_id for repo in huggingface_cache_info.repos]
    return [
        model
        for model in models
        if model.gguf_filename.strip()
        and isinstance(
            try_to_load_from_cache(
                repo_id=model.repo_id,
                filename=model.gguf_filename,
                repo_type="model",
                cache_dir=model_cache_dir,
            ),
            str,
        )
        or model.repo_id in cached_repo_names
    ]


def log_models(models, logger):
    for mdl in models:
        logger.info(f"| {mdl}")


def log_requested_models(requested_models, logger):
    logger.info("The following models were requested:")
    log_models(requested_models, logger)


def log_cached_models(cached_models, models_length, logger):
    if len(cached_models) == models_length:
        logger.info(
            "All models already found in the cache. No downloads required. Quitting..."
        )
        return

    if cached_models:
        logger.info(
            "Found models in the cache. The following will not be downloaded again:"
        )
        log_models(cached_models, logger)


def log_downloadable_models(downloadable_models, logger):
    logger.info("The following models have to be downloaded:")
    log_models(downloadable_models, logger)


def download(downloadable_models, model_cache_dir, logger):
    logger.info("Downloading models from Hugging Face...")
    for model in downloadable_models:
        gated = model.gated == "True"
        try:
            if model.gguf_filename.strip():
                logger.info(f"Downloading files for '{model.gguf_filename}'...")
                hf_hub_download(
                    repo_id=model.repo_id,
                    filename=model.gguf_filename,
                    repo_type="model",
                    cache_dir=model_cache_dir,
                    token=gated,
                )
            else:
                # Download tokenizer and tensors
                logger.info(f"Downloading files for '{model.repo_id}'...")
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
            return
        logger.info("Finished downloading the models from Hugging Face. Quitting...")


def download_models(logger):
    logging.set_verbosity_error()

    models = get_models()
    log_requested_models(models, logger)

    model_cache_dir = get_model_cache_dir()
    cached_models = get_cached_models(models, model_cache_dir)
    log_cached_models(cached_models, len(models), logger)

    downloadable_models = list(set(models) - set(cached_models))
    log_downloadable_models(downloadable_models, logger)

    confirm_action(logger, "Are you sure you want to download those models?")
    download(downloadable_models, model_cache_dir, logger)


if __name__ == "__main__":
    # Load env variable for optional API authentication
    log = get_logger()
    load_dotenv()

    download_models(log)
