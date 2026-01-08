from dataclasses import dataclass, field
from typing import Iterator, Optional, Tuple, Union


@dataclass
class Model:

    _repo_id: str
    _gguf_filename: str
    _gated: Optional[bool] = field(default=None)
    _context_length: Optional[int] = field(default=None)

    def __post_init__(self):
      if self._gated is None:
        self._gated = False
      if self._context_length is None:
        self._context_length = 0

    @property
    def repo_id(self) -> str:
      return self._repo_id

    @property
    def gguf_filename(self) -> str:
      return self._gguf_filename

    @property
    def gated(self) -> bool:
      return self._gated is True

    @property
    def name(self) -> str:
      return f"{self._repo_id}__{self._gguf_filename}"

    @property
    def context_length(self) -> int:
      return self._context_length if self._context_length else 0

    def __iter__(self) -> Iterator[Union[str, bool, int]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return f"{"(GATED) " if self._gated else ""}{self._repo_id}: {self._gguf_filename}{f" (CONTEXT LENGTH: {self.context_length})" if self._context_length else ""}"

    def _as_tuple(self) -> Tuple[str, str, bool, int]:
      return self._repo_id, self._gguf_filename, self.gated, self.context_length


