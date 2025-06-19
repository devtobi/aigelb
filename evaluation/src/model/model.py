from dataclasses import dataclass
from typing import Iterator, Tuple, Union


@dataclass
class Model:

    _repo_id: str
    _gguf_filename: str
    _gated: bool = False

    def __post_init__(self):
      if self._gated is None:
        self._gated = False

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


