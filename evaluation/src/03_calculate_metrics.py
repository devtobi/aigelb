from typing import List

from metric import Metric, MetricService
from utility import FileService, LoggingService

def calculate(metrics: List[Metric]) -> bool:
  file_paths = FileService.get_files("results/", "csv")
  for file_path in file_paths:
    filename: str = FileService.get_filename(file_path)
    LoggingService.info(f"Calculating metrics for {filename}...")

    # TODO
    lines: List[str] = FileService.from_csv(str, file_path, skip_header=False)
    for line in lines:
      LoggingService.info(line)

  return True

def calculate_metrics():
  metrics: List[Metric] = FileService.from_csv(Metric, "metrics.csv")
  if len(metrics) == 0:
    LoggingService.info("No metrics in metrics.csv. Please add some metrics first and re-run this script.")
    return
  LoggingService.log_list(metrics, "The following metrics were selected:")
  if not LoggingService.confirm_action( "Are you sure you want to start calculation with those metrics?"):
    return
  if not calculate(metrics):
    return

if __name__ == "__main__":
  ttr = MetricService.get_lexical_richness_function("ttr")
  print(ttr("Hallo das ist ein Test"))

  flesch = MetricService.get_textstat_function("flesch_reading_ease")
  print(flesch("Hallo das ist ein Test. Der Text ist sehr einfach."))

  # wiener = MetricService.get_textstat_function("wiener_sachtextformel")
  # print(wiener("Hallo das ist ein Test."))

  bleu = MetricService.get_evaluate_function("bertscore")
  print(bleu(predictions=["Hallo das ist ein Test"], references=["Hallo das ist ein Fest"]))
