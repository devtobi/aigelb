from csv import reader
from dataclasses import dataclass
from os import getenv, path
from typing import Iterator, List, Tuple, Union


@dataclass
class Model:

    repo_id: str
    gguf_filename: str
    gated: bool

    def __iter__(self) -> Iterator[Union[str, bool]]:
        return iter(self.as_tuple())

    def __str__(self) -> str:
        return (
            f"{self.repo_id}: {self.gguf_filename}"
            if self.gguf_filename
            else f"{self.repo_id}"
        )

    def as_tuple(self) -> Tuple[str, str, bool]:
      return self.repo_id, self.gguf_filename, self.gated

def get_models() -> List[Model]:
    dirname: str = path.dirname(__file__)
    model_path: str = path.join(dirname, "../../models.csv")

    with open(model_path, newline="") as csvfile:
        csv_reader: Iterator[List[str]] = reader(csvfile, delimiter=",")
        next(csv_reader, None)  # skip the headers
        return [Model(row[0], row[1], row[2] == "True") for row in csv_reader]

def get_model_cache_dir() -> str:
    return getenv("HF_HOME") or "default HuggingFace cache directory (usually ~/.cache/huggingface)"
