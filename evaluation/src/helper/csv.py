from csv import reader
from typing import Iterator, List, Type, TypeVar

from .file import get_absolute_path

T = TypeVar('T')

def from_csv(cls: Type[T], filepath: str, skip_header = True) -> List[T]:
    abs_path: str = get_absolute_path(filepath)
    with open(abs_path, newline="") as csvfile:
        csv_reader: Iterator[List[str]] = reader(csvfile, delimiter=",")
        if skip_header:
          next(csv_reader, None)
        instances = []
        for row in csv_reader:
          converted_row = [
            str_to_bool(cell) if cell.strip().lower() in ['true', 'false'] else cell
            for cell in row
          ]
          instances.append(cls(*converted_row))
        return instances

def str_to_bool(value: str) -> bool:
  if value.strip().lower() == 'true':
    return True
  elif value.strip().lower() == 'false':
    return False
  else:
    raise ValueError(f"Cannot convert '{value}' to boolean.")
