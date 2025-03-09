from dotenv import load_dotenv
from huggingface_hub import hf_hub_download, scan_cache_dir, try_to_load_from_cache
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

from helper import confirm_action, get_logger, get_model_cache_dir, get_models

# disable transformer logging for downloading
logging.set_verbosity_error()

# Load env variable for optional API authentication
logger = get_logger()
load_dotenv()

# Scan models.csv
logger.info("The following models were requested:")
models = get_models()
for model in models:
    logger.info(f"| {model}")


# Check cache
huggingface_cache_info = scan_cache_dir(cache_dir=get_model_cache_dir())
cached_repo_names = [repo.repo_id for repo in huggingface_cache_info.repos]
model_cache_dir = get_model_cache_dir()
cached_models = []
for model in models:
    if model.gguf_filename.strip() != "":
        filepath = try_to_load_from_cache(
            repo_id=model.repo_id,
            filename=model.gguf_filename,
            repo_type="model",
            cache_dir=model_cache_dir,
        )
        if isinstance(filepath, str):
            cached_models.append(model)
    else:
        if model.repo_id in cached_repo_names:
            cached_models.append(model)
if len(cached_models) == len(models):
    logger.info(
        "All models already found in the cache. No downloads required. Quitting..."
    )
    exit(1)
elif len(cached_models) != 0:
    logger.info(
        "Found some models in the cache. The following will not be downloaded again:"
    )
    for model in cached_models:
        logger.info(f"| {model}")

non_cached_models = list(set(models) - set(cached_models))
logger.info("The following models have to be downloaded:")
for model in non_cached_models:
    logger.info(f"| {model}")

# Confirm download
confirm_action(logger, "Are you sure you want to download those models?")

# Download models
logger.info("Downloading models from Hugging Face...")
for model in non_cached_models:
    gated = model.gated == "True"
    try:
        if model.gguf_filename.strip() != "":
            logger.info(f"Downloading files for '{model.gguf_filename}'...")
            hf_hub_download(
                repo_id=model.repo_id,
                filename=model.gguf_filename,
                repo_type="model",
                cache_dir=get_model_cache_dir(),
                token=gated,
            )
        else:
            # Download tokenizer and tensors
            logger.info(f"Downloading files for '{model.repo_id}...")
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
        exit(1)

logger.info("Finished downloading the models from Hugging Face. Quitting...")
