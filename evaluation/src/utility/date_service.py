from datetime import datetime


class DateService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @staticmethod
  def get_timestamp() -> str:
    return datetime.now().replace(microsecond=0).isoformat()

