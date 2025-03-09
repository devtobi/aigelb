from csv import reader
from os import path


class Model:
    def __init__(self, repo_id, gguf_filename, gated):
        self.repo_id = repo_id
        self.gguf_filename = gguf_filename
        self.gated = gated

    def __iter__(self):
        return iter((self.repo_id, self.gguf_filename, self.gated))

    def __str__(self):
        return (
            f"{self.repo_id}: {self.gguf_filename}"
            if self.gguf_filename
            else f"{self.repo_id}"
        )


def get_models():
    dirname = path.dirname(__file__)
    model_path = path.join(dirname, "../../models.csv")

    with open(model_path, newline="") as csvfile:
        csv_reader = reader(csvfile, delimiter=",")
        next(csv_reader, None)  # skip the headers
        return [Model(row[0], row[1], row[2]) for row in csv_reader]


def get_model_cache_dir():
    dirname = path.dirname(__file__)
    return path.join(dirname, "../../.cache")
