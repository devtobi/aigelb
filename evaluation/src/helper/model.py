from dataclasses import dataclass
from os import getenv
from typing import Iterator, Tuple, Union

from pathvalidate import sanitize_filename


@dataclass
class Model:

    _repo_id: str
    _gguf_filename: str
    _gated: bool

    @property
    def repo_id(self) -> str:
      return self._repo_id

    @property
    def gguf_filename(self) -> str:
      return self._gguf_filename

    @property
    def gated(self) -> bool:
      return self._gated

    @property
    def is_gguf(self) -> bool:
      return self._gguf_filename is not None and self._gguf_filename.strip() != ""

    @property
    def filename(self) -> str:
      filename = (
        f"{self._repo_id}"
        + (f"__{self._gguf_filename}" if self.is_gguf else "")
      )
      return sanitize_filename(filename, replacement_text="_")

    def __iter__(self) -> Iterator[Union[str, bool]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return (
            f"{self._repo_id}: {self._gguf_filename}"
            if self._gguf_filename
            else f"{self._repo_id}"
        )

    def _as_tuple(self) -> Tuple[str, str, bool]:
      return self._repo_id, self._gguf_filename, self._gated

def get_model_cache_dir() -> str:
    return getenv("HF_HOME") or "default HuggingFace cache directory (usually ~/.cache/huggingface)"
