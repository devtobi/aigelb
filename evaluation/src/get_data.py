from preprocess import PreprocessService
from utility import ConfigurationService, KeyboardInterruptError, LoggingService


def get_data() -> None:
  download_url = LoggingService.safe_exec_and_confirm(PreprocessService.read_download_url,
                                                "Are you sure you want to use this URL?")
  if download_url is None:
    return

  columns = LoggingService.safe_exec_and_confirm(PreprocessService.read_columns, "Are you sure you want to use those columns?")
  if columns is None:
    return

  try:
    PreprocessService.get_data(download_url, columns)
  except KeyboardInterruptError as exc:
    LoggingService.info(str(exc))
    return

if __name__ == "__main__":
    ConfigurationService.load_environment_configuration()
    get_data()
