import statistics
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

import evaluate
from lexicalrichness import LexicalRichness
from textstat import textstat

from utility import FileService, LoggingService

from .exception import (
  MetricFileEmptyError,
  MetricFileNotFoundError,
  MetricNotFoundError,
)
from .metric import Metric
from .metric_library import MetricLibrary

T = TypeVar('T')

class MetricService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @classmethod
  def get_metric_function(cls, metric_function_name: str) -> Tuple[Callable, MetricLibrary]:
    function_sources: list[Tuple[Callable[[str], Any], MetricLibrary]] = [
      (cls._get_textstat_function, MetricLibrary.TEXTSTAT),
      (cls._get_lexical_richness_function, MetricLibrary.LEXICAL_RICHNESS),
      (cls._get_evaluate_function, MetricLibrary.EVALUATE),
    ]

    for func_getter, library in function_sources:
      metric = func_getter(metric_function_name)
      if metric is not None:
        return metric, library

    raise MetricNotFoundError(f"The requested metric function '{metric_function_name}' is not available.")

  @classmethod
  def read_metric_list(cls) -> List[Metric]:
    filename = cls._get_metric_filename()
    LoggingService.info(f"Reading metrics from {filename}...")
    try:
      metrics = FileService.from_csv(Metric, filename)
      if len(metrics) == 0:
        raise MetricFileEmptyError(f"The metric file {filename} contains no valid entries.") from None
      LoggingService.log_list(metrics, "The following metrics were found:")
      return metrics
    except Exception as exc:
      raise MetricFileNotFoundError(f"The metric file '{filename}' does not exist.'") from exc

  @classmethod
  def _get_textstat_function(cls, metric_function_name: str) -> Optional[Callable]:
    if metric_function_name in cls._get_method_names(textstat):
        func = getattr(textstat, metric_function_name)

        def wrapper(text: str, lang: str = "de", *args, **kwargs):
          LoggingService.info(f"Calculating {metric_function_name} using Textstat library...")
          textstat.set_lang(lang)
          return func(text, *args, **kwargs)
        return wrapper
    return None

  @staticmethod
  def _get_evaluate_function(evaluate_metric_name: str) -> Optional[Callable]:
    try:
      metric = evaluate.load(evaluate_metric_name)
      if not hasattr(metric, "compute") or not callable(metric.compute):
        return None

      def wrapper(target: Optional[str] = None, *args, **kwargs):
        LoggingService.info(f"Calculating {evaluate_metric_name} using HuggingFace Evaluate library...")
        compute_result: Optional[Dict] = metric.compute(*args, **kwargs)
        if compute_result is None:
          raise MetricNotFoundError(f"Calculating '{evaluate_metric_name}' using HuggingFace Evaluate library failed.")
        key = evaluate_metric_name if target is None else target
        if key not in compute_result:
          raise MetricNotFoundError(f"The compute result did not contain key '{key}'.")
        result = compute_result[key]
        if type(result) is list:
          return statistics.mean(result)
        else:
          return result
      return wrapper
    except TypeError:
      return None

  @classmethod
  def _get_lexical_richness_function(cls, attribute: str) -> Optional[Callable]:
    if attribute not in cls._get_public_attributes(LexicalRichness):
      return None
    def wrapper(text: str, *args, **kwargs):
      LoggingService.info(f"Calculating {attribute} using LexicalRichness library...")
      obj = LexicalRichness(text)
      attr = getattr(obj, attribute, None)
      if not attr:
        raise MetricNotFoundError(f"Metric '{attribute}' using LexicalRichness library not found.")
      if not callable(attr):
        return attr
      else:
        return attr(*args, **kwargs)
    return wrapper

  @classmethod
  def _get_method_names(cls, obj: Any) -> List[str]:
    attributes = cls._get_public_attributes(obj)
    return [attr for attr in attributes if
                        callable(getattr(obj, attr))]

  @staticmethod
  def _get_public_attributes(obj: Any) -> List[str]:
    attributes = dir(obj)
    return [attr for attr in attributes if not attr.startswith("__")]

  @staticmethod
  def _get_metric_filename() -> str:
    return "metrics.csv"
