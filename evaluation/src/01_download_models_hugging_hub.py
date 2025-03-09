from dotenv import load_dotenv
from huggingface_hub import hf_hub_download, try_to_load_from_cache
from huggingface_hub.errors import GatedRepoError, HfHubHTTPError

from helper import confirm_action, get_logger, get_model_cache_dir, get_models

# Load env variable for optional API authentication
logger = get_logger()
load_dotenv()

# Scan models.csv
logger.info("The following models were requested:")
models = get_models()
for model in models:
    logger.info(f"| {model}")

# Check cache
model_cache_dir = get_model_cache_dir()
cached_models = []
for model in models:
    filepath = try_to_load_from_cache(
        repo_id=model.repo_id,
        filename=model.filename,
        repo_type="model",
        cache_dir=model_cache_dir,
    )
    if isinstance(filepath, str):
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
    add_token = model.gated == "True"
    try:
        hf_hub_download(
            repo_id=model.repo_id,
            filename=model.filename,
            repo_type="model",
            cache_dir=get_model_cache_dir(),
            token=add_token,
        )
    except (GatedRepoError, HfHubHTTPError):
        logger.warning(
            f'Failed downloading gated model "{model}".'
            f" Please confirm you added a valid Hugging Face access token in .env file"
            f" and are granted access to the model files."
        )
    except KeyboardInterrupt:
        exit(1)

logger.info("Finished downloading the models from Hugging Face. Quitting...")
