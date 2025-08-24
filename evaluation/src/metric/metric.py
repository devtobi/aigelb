from dataclasses import dataclass, field
from typing import Iterator, Optional, Tuple, Union


@dataclass
class Metric:

    _name: str
    _kwargs: Optional[dict[str, str | int | bool]] = field(default=None)

    def __post_init__(self):
      if self._kwargs is None:
        self._kwargs = {}

    @property
    def name(self) -> str:
      return self._name

    @property
    def kwargs(self) -> dict[str, str | int | bool]:
      return self._kwargs or {}

    def __iter__(self) -> Iterator[Union[str, dict[str, str | int | bool]]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return (
            f"{self._name}{f" with configuration {self._kwargs}" if self._kwargs != {} else ""}"
        )

    def _as_tuple(self) -> Tuple[str, dict[str, str | int | bool]]:
      return self._name, self.kwargs
