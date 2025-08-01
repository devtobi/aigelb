from utility import ConfigurationService, KeyboardInterruptError, LoggingService

ConfigurationService.load_environment_configuration()
from preprocess import PreprocessService


def get_data() -> None:
  download_url = LoggingService.safe_exec_and_confirm(PreprocessService.read_download_url,
                                                "Are you sure you want to use this URL?")
  if download_url is None:
    return

  columns = LoggingService.safe_exec_and_confirm(PreprocessService.read_column_data, "Are you sure you want to use this column configuration?")
  if columns is None:
    return

  try:
    PreprocessService.get_data(download_url, columns)
  except KeyboardInterruptError as exc:
    LoggingService.info(str(exc))
    return

if __name__ == "__main__":
    get_data()
