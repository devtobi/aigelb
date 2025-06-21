from ctypes import CFUNCTYPE, c_char_p, c_int, c_void_p
from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from sys import stdout
from typing import Callable, ClassVar, Iterable, Optional, TypeVar

from llama_cpp import (
  llama_log_set,
)

T = TypeVar('T')
LlamaLogCallbackType = Callable[[int, bytes, object], None]

class LoggingService:
  _logger: ClassVar[Optional[Logger]] = None
  _llama_log_callback: ClassVar[Optional[LlamaLogCallbackType]] = None  # hold reference to prevent GC
  _llama_mute_callback: ClassVar[Optional[LlamaLogCallbackType]] = None # hold reference to prevent GC

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @classmethod
  def _get_logger(cls) -> Logger:
    if cls._logger is None:
      logger: Logger = getLogger("aigelb-evaluation")
      logger.setLevel(INFO)

      # Prevent adding multiple handlers if the logger already has them
      if not logger.handlers:
        handler = StreamHandler(stdout)
        formatter = Formatter(
          "%(name)s - %(asctime)s - %(levelname)s - %(message)s",
          datefmt="%d.%m.%Y %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

      cls._logger = logger

    return cls._logger

  @classmethod
  def info(cls, msg: str) -> None:
    cls._get_logger().info(msg)

  @classmethod
  def error(cls, msg: str) -> None:
    cls._get_logger().error(msg)

  @classmethod
  def log_list(cls, lst: Iterable[T], msg: str = "") -> None:
    if msg:
        cls._get_logger().info(msg)
    for element in lst:
        cls._get_logger().info(f"| {element}")

  @classmethod
  def safe_exec_and_confirm(cls, read_func: Callable[[], T], confirm_msg: str) -> Optional[T]:
    try:
      result = read_func()
    except Exception as exc:
      LoggingService.error(str(exc))
      return None
    if not cls._confirm_action(confirm_msg):
      return None
    return result

  @classmethod
  def _confirm_action(cls, question: str) -> bool:
    entered: str = "none"
    while entered != "exit" and entered != "":
      print(f"{question} Press ENTER to confirm... (Type 'exit' or hit Ctrl+C to exit.) ", end="")
      try:
        entered = input()
      except KeyboardInterrupt:
        return False
    return True if not entered else False

  @classmethod
  def mute_llamacpp_logging(cls) -> None:
    def _mute_callback(level, message, user_data):
      # kept empty to mute logging output of the library
      pass
    cls._llama_mute_callback = _mute_callback

    # Mute logging for verbose llama-cpp output, no type information required
    cls._llama_log_callback = CFUNCTYPE(None, c_int, c_char_p, c_void_p)(cls._llama_mute_callback)
    # pyrefly: ignore
    llama_log_set(cls._llama_log_callback, c_void_p())
