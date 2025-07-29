from ast import literal_eval
from csv import QUOTE_ALL, DictReader, DictWriter, reader, writer
from json import JSONDecodeError, loads
from os import listdir, makedirs, path, remove
from typing import Any, List, LiteralString, Optional, Protocol, Type, TypeVar, cast

from pathvalidate import sanitize_filename


class DictSerializable(Protocol):
  def to_dict(self) -> dict: ...

T = TypeVar('T')
S = TypeVar('S', bound=DictSerializable)

class FileService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @classmethod
  def from_csv(cls, item_type: Type[T], filepath: str, column_name: Optional[str] = None) -> List[T]:
    abs_path: str = cls.get_absolute_path(filepath)
    with open(abs_path, mode="r", newline="", encoding="utf-8") as csvfile:
      dict_reader = DictReader(csvfile)

      if column_name:
        return [row[column_name] for row in dict_reader if column_name in row]

      instances = []
      for row in dict_reader:
        processed_row = cls._process_row(row)
        instance = item_type(**processed_row)
        instances.append(instance)
      return instances

  @classmethod
  def from_csv_to_string_list(cls, filepath: str) -> List[str]:
    abs_path: str = cls.get_absolute_path(filepath)
    with open(abs_path, mode="r", newline="", encoding="utf-8") as csvfile:
      csv_reader = reader(csvfile)
      return [row[0] for row in csv_reader if row and row[0].strip()]

  @classmethod
  def from_file_to_string(cls, filepath: str) -> str:
    abs_path: str = cls.get_absolute_path(filepath)
    with open(abs_path, mode="r", newline="", encoding='utf-8') as file:
      return file.read()

  @classmethod
  def to_csv(cls, rows: List[S], filepath: str, simple_list: bool = False) -> None:
    if len(rows) == 0:
      raise ValueError("Cannot write empty row list to CSV")

    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)

    with open(abs_path, mode='w', newline='') as csvfile:
      if simple_list:
        csv_writer = writer(csvfile, quoting=QUOTE_ALL)
        for item in rows:
          csv_writer.writerow([item])  # Wrap in a list to treat as a row
      else:
        fieldnames = set()
        for row in rows:
          fieldnames.update(row.to_dict().keys())
        fieldnames = sorted(fieldnames)
        dict_writer = DictWriter(csvfile, fieldnames=fieldnames, quoting=QUOTE_ALL)
        dict_writer.writeheader()
        for row in rows:
          dict_writer.writerow(row.to_dict())

  @classmethod
  def to_file(cls, filepath: str, content: str) -> None:
    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)
    with open(abs_path, mode="w", newline="", encoding='utf-8') as file:
      file.write(content)

  @classmethod
  def to_file_bytes(cls, filepath: str, content: bytes) -> None:
    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)
    with open(abs_path, mode="wb") as file:
      file.write(content)

  @classmethod
  def delete_file(cls, filepath) -> None:
    abs_path: str = cls.get_absolute_path(filepath)
    if path.exists(abs_path):
      remove(abs_path)

  @classmethod
  def exists_file(cls, filepath) -> bool:
    abs_path: str = cls.get_absolute_path(filepath)
    return path.exists(abs_path)

  @classmethod
  def count_csv_lines(cls, filepath: str) -> int:
    abs_path: str = cls.get_absolute_path(filepath)
    with open(abs_path, mode="r", newline="", encoding="utf-8") as file:
      csv_reader = reader(file)
      return sum(1 for _ in csv_reader)

  @classmethod
  def append_to_csv(cls, filepath: str, row: Any | List[Any]) -> None:
    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)
    with open(abs_path, mode="a", newline="", encoding="utf-8") as file:
      file_writer = writer(file, quoting=QUOTE_ALL)
      if isinstance(row, list):
        file_writer.writerow(row)
      else:
        file_writer.writerow([row])

  @staticmethod
  def extract_value_from_json(json_string: str, key: str) -> str:
    try:
      json_representation = loads(json_string)
      return json_representation[key]
    except JSONDecodeError:
      return ""

  @classmethod
  def get_directories(cls, dirpath: str) -> List[str]:
    abs_path = cls.get_absolute_path(dirpath)
    return [
      entry for entry in listdir(abs_path)
      if path.isdir(path.join(cast(LiteralString, abs_path), cast(LiteralString,entry)))
    ]

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

  @staticmethod
  def sanitize_file_name(filename: str) -> str:
    return sanitize_filename(filename, replacement_text="_")

  @staticmethod
  def get_absolute_path(pth: str) -> str:
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


