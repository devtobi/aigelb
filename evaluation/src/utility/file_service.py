from ast import literal_eval
from csv import QUOTE_ALL
from io import StringIO
from os import listdir, makedirs, path, remove
from typing import Any, List, LiteralString, Optional, Protocol, Type, TypeVar, cast

from pandas import DataFrame, json_normalize, notna, read_csv, read_json
from pathvalidate import sanitize_filename


class DictSerializable(Protocol):
  def to_dict(self) -> dict: ...

T = TypeVar('T')
S = TypeVar('S', bound=DictSerializable)

class FileService:

  def __new__(cls, *args, **kwargs):
    raise TypeError("This utility class cannot be instantiated.")

  @classmethod
  def from_csv(cls, item_type: Type[T], filepath: str, column_name: Optional[str] = None, separator: str = ",") -> List[T]:
    abs_path: str = cls.get_absolute_path(filepath)
    df = read_csv(abs_path, sep=separator, encoding="utf-8")

    # Replace pandas nan with None
    df = df.astype(object).where(df.notna(), None)

    if column_name:
      return [cast(T, val) for val in df[column_name]]

    instances = []
    for row in df.to_dict(orient="records"):
      processed_row = cls._process_row(row)
      instance = item_type(**processed_row)
      instances.append(instance)
    return instances

  @classmethod
  def from_csv_to_string_list(cls, filepath: str) -> List[str]:
    abs_path: str = cls.get_absolute_path(filepath)
    df = read_csv(abs_path, header=None, sep=",", encoding="utf-8")
    return [str(val).strip() for val in df.iloc[:, 0] if notna(val) and str(val).strip()]

  @classmethod
  def from_file_to_string(cls, filepath: str) -> str:
    abs_path: str = cls.get_absolute_path(filepath)
    with open(abs_path, mode="r", newline="", encoding='utf-8') as file:
      return file.read()

  @classmethod
  def to_csv(cls, rows: List[S], filepath: str, simple_list: bool = False) -> None:
    if not rows:
      raise ValueError("Cannot write empty row list to CSV")

    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)

    if simple_list:
      df = DataFrame([[item] for item in rows])
    else:
      df = DataFrame([row.to_dict() for row in rows])

    df.to_csv(abs_path, index=False, header=not simple_list, quoting=QUOTE_ALL)

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
    df = read_csv(abs_path, sep=",", encoding="utf-8", header=None)
    return len(df)

  @classmethod
  def append_to_csv(cls, filepath: str, row: Any | List[Any]) -> None:
    abs_path: str = cls.get_absolute_path(filepath)
    makedirs(path.dirname(abs_path), exist_ok=True)

    row_data = [row] if isinstance(row, list) else [[row]]
    df = DataFrame(row_data)
    df.to_csv(abs_path, mode="a", index=False, header=False, quoting=QUOTE_ALL)

  @staticmethod
  def extract_value_from_json(json_string: str, key: str) -> str:
    try:
      buf = StringIO(json_string)
      json_series = read_json(buf, typ='series', orient='index')
      df = json_normalize([json_series.to_dict()])
      return str(df.at[0, key])
    except (ValueError, KeyError, TypeError):
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
      # Pass through None
      if val is None:
        result[key] = None
        continue

      # Convert non-string values to string (if needed) for uniform processing
      if isinstance(val, str):
        val_str = val.strip()
      else:
        val_str = str(val).strip()

      # Try to convert boolean-like strings
      if val_str.lower() in ['true', 'false']:
        result[key] = cls._str_to_bool(val_str)
      # Try to parse lists, dicts, or numeric values
      elif val_str.startswith('{') or val_str.startswith('[') or val_str.isdigit():
        try:
          result[key] = literal_eval(val_str)
        except (ValueError, SyntaxError):
          result[key] = val_str  # Fallback to cleaned string
      else:
        result[key] = val_str
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
