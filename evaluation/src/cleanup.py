from logging import Logger
from typing import List

from huggingface_hub import (
    CacheNotFound,
    DeleteCacheStrategy,
    HFCacheInfo,
    scan_cache_dir,
)

from helper import confirm_action, get_logger


def clear_cache(logger: Logger) -> None:
    # Read local cache
    try:
        huggingface_cache_info: HFCacheInfo = scan_cache_dir()
    except CacheNotFound:
        logger.info("No cache folder found. Download some models first. Quitting...")
        return

    # Extract revision commit hashes
    revisions: List[str] = [
        revision.commit_hash
        for repo in huggingface_cache_info.repos
        for revision in repo.revisions
    ]

    if not revisions:
        logger.info("Found no models in cache. Nothing to clear. Quitting...")
        return

    # Prepare deletion operation
    delete_operation: DeleteCacheStrategy = huggingface_cache_info.delete_revisions(*revisions)
    logger.info(
        f"Found {len(revisions)} models in cache."
        f" Freeing will re-claim {delete_operation.expected_freed_size_str}B"
    )

    # Confirm before deletion
    if not confirm_action(logger, "Do you want to delete those models now?"):
        return

    # Execute deletion
    delete_operation.execute()
    logger.info("Successfully cleared the cache. Quitting...")


if __name__ == "__main__":
    log = get_logger()
    clear_cache(log)
