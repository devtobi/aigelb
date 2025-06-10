from dataclasses import dataclass
from os import getenv
from typing import Iterator, Tuple, Union


@dataclass
class Model:

    repo_id: str
    gguf_filename: str
    gated: bool

    def __iter__(self) -> Iterator[Union[str, bool]]:
        return iter(self.as_tuple())

    def __str__(self) -> str:
        return (
            f"{self.repo_id}: {self.gguf_filename}"
            if self.gguf_filename
            else f"{self.repo_id}"
        )

    def as_tuple(self) -> Tuple[str, str, bool]:
      return self.repo_id, self.gguf_filename, self.gated

def get_model_cache_dir() -> str:
    return getenv("HF_HOME") or "default HuggingFace cache directory (usually ~/.cache/huggingface)"
