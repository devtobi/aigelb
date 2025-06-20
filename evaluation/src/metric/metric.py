from dataclasses import dataclass, field
from typing import Iterator, Tuple, Union


@dataclass
class Metric:

    _name: str
    _is_corpus_level: bool
    _kwargs: dict[str, str | int | bool] = field(default_factory=lambda: {})

    def __post_init__(self):
      if self._kwargs is None:
        self._kwargs = {}

    @property
    def name(self) -> str:
      return self._name

    @property
    def is_corpus_level(self) -> bool:
      return self._is_corpus_level

    @property
    def kwargs(self) -> dict[str, str | int | bool]:
      return self._kwargs

    def __iter__(self) -> Iterator[Union[str, bool, dict[str, str | int | bool]]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return (
            f"{self._name}{f" with configuration {self._kwargs}" if self._kwargs != {} else ""} on {"corpus level" if self._is_corpus_level else 'sentence level'}"
        )

    def _as_tuple(self) -> Tuple[str, bool, dict[str, str | int | bool]]:
      return self._name, self._is_corpus_level, self._kwargs
