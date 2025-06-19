from dataclasses import dataclass
from typing import Iterator, Tuple, Union


@dataclass
class CalculationResult:

    _model_name: str
    _metric_results: dict[str, float]

    @property
    def model_name(self) -> str:
      return self._model_name

    @property
    def metric_results(self) -> dict[str, float]:
      return self._metric_results

    def to_dict(self) -> dict:
      return {'_model_name': self._model_name, **self._metric_results}

    def __iter__(self) -> Iterator[Union[str, dict[str, float]]]:
        return iter(self._as_tuple())

    def __str__(self) -> str:
        return (
            f"Result for {self._model_name} with {self._metric_results}"
        )

    def _as_tuple(self) -> Tuple[str, dict[str, float]]:
      return self._model_name, self._metric_results




