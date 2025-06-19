import statistics
from collections.abc import Callable
from typing import List, Optional

from metric import Metric, MetricService

from .exception import CalculationDataLengthMismatchError, CalculationMetricError


class CalculationService:

    def __new__(cls, *args, **kwargs):
      raise TypeError("This class cannot be instantiated.")

    @classmethod
    def calculate_metric(cls, metric: Metric, references: List[str], predictions: Optional[List[str]] = None) -> float:
      function, _ = MetricService.get_metric_function(metric.name)
      if predictions is not None and len(predictions) != len(references):
        raise CalculationDataLengthMismatchError("Length of references and predictions did not match!")
      if (predictions is None) or (len(predictions) == 0):
        return cls._calculate_no_references(references, function, metric)
      else:
        return cls._calculate_with_references(references, predictions, function, metric)

    @staticmethod
    def _calculate_no_references(texts: List[str], func: Callable, metric: Metric) -> float:
      try:
        if not metric.is_corpus_level:
          results = []
          for text in texts:
            result = func(text, **metric.kwargs)
            results.append(result)
          return statistics.mean(results)
        else:
          text = ' '.join(texts)
          return func(text, **metric.kwargs)
      except Exception as exc:
        raise CalculationMetricError(f"Error calculating {metric.name}!") from exc


    @staticmethod
    def _calculate_with_references(references: List[str], predictions: List[str], func: Callable, metric: Metric) -> float:
      if not metric.is_corpus_level:
        results = []
        for idx, reference in enumerate(references):
          result = func(references=[reference], predictions=[predictions[idx]], **metric.kwargs)
          results.append(result)
        return statistics.mean(results)
      else:
        return func(references=references, predictions=predictions, **metric.kwargs)


