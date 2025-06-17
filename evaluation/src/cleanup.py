from typing import List

from huggingface_hub import (
    CacheNotFound,
    DeleteCacheStrategy,
    HFCacheInfo,
    scan_cache_dir,
)

from utility import LoggingService, confirm_action


def clear_cache() -> None:
    # Read local cache
    try:
        huggingface_cache_info: HFCacheInfo = scan_cache_dir()
    except CacheNotFound:
        LoggingService.info("No cache folder found. Quitting...")
        return

    # Extract revision commit hashes
    revisions: List[str] = [
        revision.commit_hash
        for repo in huggingface_cache_info.repos
        for revision in repo.revisions
    ]

    if not revisions:
        LoggingService.info("Found no models in cache. Nothing to clear. Quitting...")
        return

    # Prepare deletion operation
    delete_operation: DeleteCacheStrategy = huggingface_cache_info.delete_revisions(*revisions)
    LoggingService.info(
        f"Found {len(revisions)} models in cache."
        f" Freeing will re-claim {delete_operation.expected_freed_size_str}B"
    )

    if not confirm_action("Do you want to delete those models now?"):
        return
    delete_operation.execute()
    LoggingService.info("Successfully cleared the cache. Quitting...")


if __name__ == "__main__":
    clear_cache()
