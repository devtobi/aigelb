from typing import List

from calculation import CalculationService
from metric import Metric, MetricService
from model import Model, ModelService
from utility import KeyboardInterruptError, LoggingService


def calculate_metrics():
  try:
    models: List[Model] = ModelService.read_model_list()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use those models for calculation?"):
    return
  try:
    metrics: List[Metric] = MetricService.read_metric_list()
  except Exception as exc:
    LoggingService.error(str(exc))
    return
  if not LoggingService.confirm_action("Are you sure you want to use those metrics for calculation?"):
    return
  try:
    CalculationService.calculate_metrics(models, metrics)
  except KeyboardInterruptError as exc:
    LoggingService.error(str(exc))
    return

if __name__ == "__main__":
  calculate_metrics()
