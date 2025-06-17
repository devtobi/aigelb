from glob import glob
from os import path
from typing import List


def get_absolute_path(pth: str) -> str:
  this = path.abspath(__file__)
  root = path.dirname(path.dirname(path.dirname(this)))
  return path.join(root, pth)

def get_files(pth: str, extension: str) -> List[str]:
  abs_path = get_absolute_path(pth)
  return glob(f"{abs_path}/*.{extension}")

def get_filename(filepath: str) -> str:
  return path.basename(filepath)
