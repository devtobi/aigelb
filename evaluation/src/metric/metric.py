from dataclasses import dataclass
from typing import Iterator, Tuple, Union


@dataclass
class Metric:

    _name: str
    _library: str
    _is_corpus_level: bool

    @property
    def name(self) -> str:
      return self._name

    def library(self) -> str:
      return self._library

    @property
    def is_corpus_level(self) -> bool:
      return self._is_corpus_level

    def __iter__(self) -> Iterator[Union[str, bool]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return (
            f"{self._name} from {self._library} on {"corpus level" if self._is_corpus_level else 'sentence level'}"
        )

    def _as_tuple(self) -> Tuple[str, str, bool]:
      return self._name, self._library, self._is_corpus_level
