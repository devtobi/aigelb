from ast import literal_eval
from csv import DictReader
from glob import glob
from os import path
from typing import List, Type, TypeVar

T = TypeVar('T')

class FileService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @classmethod
  def from_csv(cls, item_type: Type[T], filepath: str, skip_header=True) -> List[T]:
    abs_path: str = cls._get_absolute_path(filepath)
    with open(abs_path, newline="") as csvfile:
      dict_reader = DictReader(csvfile, delimiter=",")
      instances = []
      for row in dict_reader:
        processed_row = cls._process_row(row)
        instance = item_type(**processed_row)
        instances.append(instance)
      return instances

  @classmethod
  def _process_row(cls, row: dict) -> dict:
    result = {}
    for key, val in row.items():
      # Check if is None
      if val is None:
        result[key] = None
        continue
      val = val.strip()
      # Try converting to bool
      if val.lower() in ['true', 'false']:
        result[key] = cls._str_to_bool(val)
      # Try converting dict/list/number via literal_eval
      elif val.startswith('{') or val.startswith('[') or val.isdigit():
        try:
          result[key] = literal_eval(val)
        except (ValueError, SyntaxError):
          result[key] = val  # Fallback to string if it fails
      else:
        result[key] = val
    return result

  @classmethod
  def get_files(cls, pth: str, extension: str) -> List[str]:
    abs_path = cls._get_absolute_path(pth)
    return glob(f"{abs_path}/*.{extension}")

  @staticmethod
  def get_filename(filepath: str) -> str:
    return path.basename(filepath)

  @staticmethod
  def _get_absolute_path(pth: str) -> str:
    this = path.abspath(__file__)
    root = path.dirname(path.dirname(path.dirname(this)))
    return path.join(root, pth)

  @staticmethod
  def _str_to_bool(value: str) -> bool:
    if value.strip().lower() == 'true':
      return True
    elif value.strip().lower() == 'false':
      return False
    else:
      raise ValueError(f"Cannot convert '{value}' to boolean.")


