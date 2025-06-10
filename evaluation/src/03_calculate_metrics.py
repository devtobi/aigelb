from logging import Logger
from typing import List

from helper import Metric, confirm_action, from_csv, get_logger, log_list


def calculate(metrics: List[Metric], logger: Logger) -> bool:
  return True

def calculate_metrics(logger: Logger):
  metrics: List[Metric] = from_csv(Metric, "metrics.csv")
  if len(metrics) == 0:
    logger.info("No metrics in metrics.csv. Please add some metrics first and re-run this script.")
    return
  log_list(metrics, logger, "The following metrics were selected:")
  if not confirm_action(logger, "Are you sure you want to start calculation with those metrics?"):
    return
  if not calculate(metrics, logger):
    return

if __name__ == "__main__":
    # Load env variable for optional API authentication
    log: Logger = get_logger()

    calculate_metrics(log)
