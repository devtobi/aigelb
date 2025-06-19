from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

import evaluate
import textstat
from lexicalrichness import LexicalRichness

from .exception import MetricNotFoundError
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
  def _get_textstat_function(cls, metric_function_name: str) -> Optional[Callable]:
    if metric_function_name in cls._get_method_names(textstat):
      return getattr(textstat, metric_function_name)
    return None

  @staticmethod
  def _get_evaluate_function(evaluate_metric_name: str) -> Optional[Callable]:
    try:
      metric = evaluate.load(evaluate_metric_name)
      if not hasattr(metric, "compute") or not callable(metric.compute):
        return None

      def compute_wrapper(*args, **kwargs):
        result: Optional[Dict] = metric.compute(*args, **kwargs)
        if result is None:
          raise MetricNotFoundError(f"Computing '{evaluate_metric_name}' from evaluate library failed.")
        if evaluate_metric_name not in result:
          raise MetricNotFoundError(f"The compute result did not contain key '{evaluate_metric_name}'.")
        return result[evaluate_metric_name]

      return compute_wrapper
    except TypeError:
      return None

  @classmethod
  def _get_lexical_richness_function(cls, attribute: str) -> Optional[Callable]:
    if attribute not in cls._get_public_attributes(LexicalRichness):
      return None
    def wrapper(text, *args, **kwargs):
      obj = LexicalRichness(text)
      attr = getattr(obj, attribute, None)
      if not attr:
        raise MetricNotFoundError(f"Metric '{attribute}' from Lexical Richness not found.")
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
