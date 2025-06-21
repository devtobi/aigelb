
from calculation import CalculationService
from metric import MetricService
from model import ModelService
from utility import KeyboardInterruptError, LoggingService


def calculate_metrics():
  models = LoggingService.safe_exec_and_confirm(ModelService.read_model_list, "Are you sure you want to use those models for calculation?")
  if models is None:
    return

  metrics = LoggingService.safe_exec_and_confirm(MetricService.read_metric_list, "Are you sure you want to use those metrics for calculation?")
  if models is None:
    return

  try:
    CalculationService.calculate_metrics(models, metrics)
  except KeyboardInterruptError as exc:
    LoggingService.error(str(exc))
    return

if __name__ == "__main__":
  calculate_metrics()
