from typing import Any, Dict, List, Optional, TypeVar

import evaluate
import textstat
from lexicalrichness import LexicalRichness

from metric.exception import MetricNotFoundError

T = TypeVar('T')

_dispatch = {
    'textstat': textstat,
    'evaluate': evaluate,          # package
    'lexrich': LexicalRichness,    # class
}

class MetricService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This class cannot be instantiated.")

  @classmethod
  def get_textstat_function(cls, metric_function_name: str) -> Any:
    if metric_function_name in cls._get_method_names(textstat):
      return getattr(textstat, metric_function_name)
    return None

  @staticmethod
  def get_evaluate_function(evaluate_metric_name: str) -> Any:
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
  def get_lexical_richness_function(cls, attribute: str) -> Any:
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
