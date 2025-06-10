from dataclasses import dataclass
from typing import Iterator, Tuple, Union


@dataclass
class Metric:

    name: str
    is_corpus_level: bool

    def __iter__(self) -> Iterator[Union[str, bool]]:
        return iter(self.as_tuple())

    def __str__(self) -> str:
        return (
            f"{self.name} on {"corpus level" if self.is_corpus_level else 'sentence level'}"
        )

    def as_tuple(self) -> Tuple[str, bool]:
      return self.name, self.is_corpus_level
