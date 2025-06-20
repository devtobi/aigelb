import statistics
from collections.abc import Callable
from typing import List, Optional

from metric import Metric, MetricLibrary, MetricService
from model import Model, ModelService
from utility import DateService, FileService, LoggingService

from .calculation_result import CalculationResult
from .exception import (
    CalculationDataLengthMismatchError,
    CalculationMetricError,
    CalculationReferenceFileNotFoundError,
    CalculationResultsWriteError,
)


class CalculationService:

    def __new__(cls, *args, **kwargs):
      raise TypeError("This class cannot be instantiated.")

    @classmethod
    def calculate_metrics(cls, models: List[Model], metrics: List[Metric]):
      print("NOT IMPLEMENTED YET")

    @classmethod
    def calculate_result_for_model(cls, model: Model, metrics: List[Metric]) -> CalculationResult:
      references = cls._read_references_file()
      predictions = cls._read_predictions_file(model)
      metric_results = {}
      for metric in metrics:
        LoggingService.info(f"Calculating {metric.name} for {model.name}")
        result = cls._calculate_metric(metric, references, predictions)
        metric_results[metric.name] = result
      return CalculationResult(_model_name=model.name, _metric_results=metric_results)

    @classmethod
    def write_calculation_results(cls, results: List[CalculationResult]):
      timestamp: str = DateService.get_timestamp()
      timestamp_sanitized = FileService.sanitize_file_name(timestamp)
      filename = f"result_{timestamp_sanitized}.csv"
      filepath = f"{cls._get_results_directory()}/{filename}"
      LoggingService.info(f"Writing calculation results to {filepath}")
      try:
        FileService.to_csv(results, filepath)
      except Exception as exc:
        raise CalculationResultsWriteError("Error writing calculation results to file") from exc

    @classmethod
    def _calculate_metric(cls, metric: Metric, references: List[str], predictions: Optional[List[str]] = None) -> float:
      function, library = MetricService.get_metric_function(metric.name)
      if predictions is not None and len(predictions) != len(references):
        raise CalculationDataLengthMismatchError("Length of references and predictions did not match!")
      used_predictions = predictions if library is MetricLibrary.EVALUATE else None
      if (used_predictions is None) or (len(used_predictions) == 0):
        return cls._calculate_no_references(references, function, metric)
      else:
        return cls._calculate_with_references(references, used_predictions, function, metric)

    @classmethod
    def _read_references_file(cls) -> List[str]:
      filename = cls._get_reference_file()
      LoggingService.info(f"Reading references from {filename}")
      try:
        return FileService.from_csv_to_string_list(filename)
      except Exception as exc:
        raise CalculationReferenceFileNotFoundError("Error reading references from file") from exc

    @classmethod
    def _read_predictions_file(cls, model: Model) -> List[str]:
      filename = f"{ModelService.get_filename(model)}.csv"
      filepath = f"{cls._get_predictions_directory()}/{filename}"
      LoggingService.info(f"Reading predictions from {filepath}")
      try:
        return FileService.from_csv_to_string_list(filepath)
      except Exception as exc:
        raise CalculationReferenceFileNotFoundError("Error reading references from file") from exc

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

    @staticmethod
    def _get_results_directory() -> str:
      return "results"

    @staticmethod
    def _get_predictions_directory() -> str:
      return "predictions"

    @staticmethod
    def _get_reference_file() -> str:
      return "references.csv"
