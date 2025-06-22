from collections.abc import Callable
from typing import List, Optional

from tqdm import tqdm

from generation import GenerationService
from metric import Metric, MetricLibrary, MetricService
from model import Model, ModelService
from utility import (
    ConfigurationService,
    DateService,
    FileService,
    KeyboardInterruptError,
    LoggingService,
)

from .calculation_result import CalculationResult
from .exception import (
    CalculationDataLengthMismatchError,
    CalculationMetricError,
    CalculationPredictionsFileNotFoundError,
    CalculationReferenceFileNotFoundError,
    CalculationResultsWriteError,
)


class CalculationService:

    def __new__(cls, *args, **kwargs):
      raise TypeError("This class cannot be instantiated.")

    @classmethod
    def calculate_metrics(cls, models: List[Model], metrics: List[Metric]):
      calculation_results: List[CalculationResult] = []

      LoggingService.info("Calculating metrics for source...")
      calculation_results.append(cls._calculate_result_for_source(metrics))

      LoggingService.info("Calculating metrics for reference...")
      calculation_results.append(cls._calculate_result_for_reference(metrics))

      LoggingService.info("Calculating metrics for models...")
      try:
        with tqdm(models) as pbar:
          for model in pbar:
            pbar.set_description(model.name)
            result = cls._calculate_result_for_model(model, metrics)
            calculation_results.append(result)
      except KeyboardInterrupt:
        raise KeyboardInterruptError("The calculation was interrupted by keyboard. Please re-run script to restart calculation.") from None

      cls._write_calculation_results(calculation_results)

    @classmethod
    def _calculate_result_for_model(cls, model: Model, metrics: List[Metric]) -> CalculationResult:
      references = cls._read_references_file()
      predictions = cls._read_predictions_file(model)
      return cls._calculate_result(model.name, metrics, predictions, references)

    @classmethod
    def _calculate_result_for_reference(cls, metrics: List[Metric]) -> CalculationResult:
      references = cls._read_references_file()
      model_name = "reference"
      return cls._calculate_result(model_name, metrics, predictions=references)

    @classmethod
    def _calculate_result_for_source(cls, metrics: List[Metric]) -> CalculationResult:
      sources = GenerationService.read_source_file()
      model_name = "source"
      return cls._calculate_result(model_name, metrics, predictions=sources)

    @classmethod
    def _calculate_result(cls, model_name: str, metrics: List[Metric], predictions: List[str], references: Optional[List[str]] = None) -> CalculationResult:
      metric_results = {}

      with tqdm(metrics, leave=False) as pbar:
        for metric in pbar:
          metric_csv_name = MetricService.get_metric_csv_name(metric)
          pbar.set_description(f"-> {metric_csv_name}")
          metric_results[metric_csv_name] = cls._calculate_metric(metric, predictions=predictions, references=references)

      return CalculationResult(_model_name=model_name, _metric_results=metric_results)

    @classmethod
    def _write_calculation_results(cls, results: List[CalculationResult]):
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
    def _calculate_metric(cls, metric: Metric, predictions: List[str], references: Optional[List[str]] = None) -> Optional[float]:
      function, library = MetricService.get_metric_function(metric.name)
      if references is not None and len(predictions) != len(references):
        raise CalculationDataLengthMismatchError("Length of references and predictions did not match!")
      if library is MetricLibrary.EVALUATE and references is None:
        return None
      used_references = references if library is MetricLibrary.EVALUATE else None
      if (used_references is None) or (len(used_references) == 0):
        return cls._calculate_no_references(predictions, function, metric)
      else:
        return cls._calculate_with_references(predictions, used_references, function, metric)

    @classmethod
    def _read_references_file(cls) -> List[str]:
      filename = cls._get_reference_filepath()
      try:
        return FileService.from_csv_to_string_list(filename)
      except Exception as exc:
        raise CalculationReferenceFileNotFoundError(f"The references file '{filename}' does not exist.") from exc

    @classmethod
    def _read_predictions_file(cls, model: Model) -> List[str]:
      filename = f"{ModelService.get_filename(model)}.csv"
      filepath = f"{GenerationService.get_predictions_directory()}/{filename}"
      try:
        return FileService.from_csv_to_string_list(filepath)
      except Exception as exc:
        raise CalculationPredictionsFileNotFoundError(f"The references file '{filename}' does not exist.") from exc

    @staticmethod
    def _calculate_no_references(texts: List[str], func: Callable, metric: Metric) -> float:
      try:
        combined_text = ' '.join(texts)
        return func(combined_text, **metric.kwargs)
      except Exception as exc:
        raise CalculationMetricError(f"Error calculating {metric.name}!") from exc

    @staticmethod
    def _calculate_with_references(predictions: List[str], references: List[str], func: Callable, metric: Metric) -> float:
      try:
        return func(predictions=predictions, references=references, **metric.kwargs)
      except Exception as exc:
        raise CalculationMetricError(f"Error calculating {metric.name}!") from exc

    @staticmethod
    def _get_results_directory() -> str:
      return "results"

    @staticmethod
    def _get_reference_filepath() -> str:
      return f"{ConfigurationService.get_data_directory()}/references.csv"
