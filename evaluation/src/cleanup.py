from huggingface_hub import CacheNotFound, scan_cache_dir

from helper import confirm_action, get_logger, get_model_cache_dir

logger = get_logger()

# Read local cache
try:
    huggingface_cache_info = scan_cache_dir(cache_dir=get_model_cache_dir())
except CacheNotFound:
    logger.info("No cache folder found. Download some models first. Quitting...")
    exit(1)

# Get revision commit hashes
repos = huggingface_cache_info.repos
revisions = [revision.commit_hash for repo in repos for revision in repo.revisions]
model_amount = len(revisions)
if model_amount == 0:
    logger.info("Found no models in cache. Nothing to clear. Quitting...")
    exit(1)

# Prepare delete operation
delete_operation = huggingface_cache_info.delete_revisions(*revisions)
logger.info(
    f"Found {model_amount} models in cache."
    f" Freeing would re-claim {delete_operation.expected_freed_size_str}B"
)

# Delete cache
confirm_action(logger, "Do you want to delete those models now?")
delete_operation.execute()
logger.info("Successfully cleared the cache. Quitting...")
