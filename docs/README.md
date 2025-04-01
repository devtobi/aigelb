[![Last commit][commit-shield]][commit-url]
[![License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/devtobi/aigelb">
    <img src="./assets/logo.png" alt="AIGELB logo" width="128" height="129">
  </a>

  <h3 align="center">AIGELB</h3>

  <p align="center">
    <b>AI</b> <b>G</b>erman <b>E</b>asy <b>L</b>anguage <b>B</b>rowsing
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* Browser Extension
  * [Installation](#installation)
  * [Usage](#usage)
* Evaluation
  * [Installation](#installation-1)
  * [Usage](#usage-1)
* [Authors](#authors)
* [License](#license)
* [Citation](#citation)

<!-- ABOUT THE PROJECT -->
## About The Project

This project was created as part of my [master thesis](#citation)
in Computer Science at the [Munich University of Applied Sciences](https://hm.edu/en/).
It contains two different parts which are as follows:

* `browser-extension`: Implementation of a browser extension using local LLMs
to translate web content into German "Easy Language", also known as "Leichte Sprache".
* `evaluation`: Python-based scripts to check the suitability
of different LLMs in regard to the use case "Easy Language" in German.

### Built With

#### Evaluation

* [Python](https://www.python.org)
* [Poetry](https://python-poetry.org)
* [HuggingFace Hub](https://huggingface.co)
* [LangChain](https://www.langchain.com)
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
* [llama-cpp-python](https://llama-cpp-python.readthedocs.io)

#### Browser extension

* [TypeScript](https://www.typescriptlang.org)
* [Bun](https://bun.sh)
* [Vue](https://vuejs.org)
* [Vuetify](https://vuetifyjs.com)
* [WXT](https://wxt.dev)

## Browser Extension

### Installation

TODO

### Usage

TODO

## Evaluation

### Installation

The execution of the Python scripts require you to have a modern version of

* Python as programming language and
* Poetry as dependency management tool

installed on your system.
Please check out the [Python documentation](https://www.python.org/downloads)
and [Poetry documentation](https://python-poetry.org/docs/#installation)
for installation instructions.

The exact compatible versions of Python and Poetry
can be found in the `pyproject.toml` file inside the `evaluation` directory.

When the requirements above are met,
you only need to execute `poetry install` inside the `evaluation` directory
to download the required packages.

### Usage

All mentioned scripts can be run via poetry
using the following command: `poetry run python <script-name>.py`

#### Configuration Setup

Before starting the evaluation, you can define which models you want to evaluate
inside the `models.csv` file in the `evaluation` directory.
You can only use models from the [HuggingFace](https://huggingface.co) platform.

The file has the following columns:

* `huggingface_repo`: repository name of the model (e.g. [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it)).
* `gguf_filename` (optional): Only required when a `.gguf` based model
should be download from the repository;
if kept empty will assume `huggingface_repo` is a standard model compatible with
the [transformers](https://huggingface.co/docs/transformers/index) library.
* `gated`: `True` or `False` whether the model is gated
(e.g. when a license agreement consent on HuggingFace
platform is necessary for your account).

The `.env` file inside the `evaluation` directory
allows further customization of the evaluation behaviour.
Relevant environment variables are the following:

* `HF_TOKEN` (optional): HuggingFace token for your account
to fetch gated models that you approved on the platform.
See [HuggingFace documentation](https://huggingface.co/docs/hub/security-tokens)
for further information.
* `USE_CPU`: `True` or `False` whether you want to use your CPU or GPU for LLM inference.

**Note:** To make GPU inference work on your machine,
you might have to do additional steps to use your GPU backend
in `llama-cpp-python` (for GGUF inference).
See [official documentation](https://llama-cpp-python.readthedocs.io/en/latest/#supported-backends)
for further information.
`transformers` should auto-detect your GPU backend
due to PyTorch being used under the hood.

### 1. Downloading models

To download the models you selected for evaluation,
you need to run the download script
using `poetry run python src/01_download_models.py`
when you are inside the `evaluation` directory.

The script will read the content of the `models.csv` file
and ask you to confirm the download before starting.

The downloaded models will be stored in the `.cache` folder
inside the `evaluation` directory for later use.

**Tip:** If you interrupt the model downloads by quitting the script execution,
the script will automatically resume the downloads where they stopped.

#### Clean up

When you experiment with different models
your `.cache` folder might fill up quickly
and unused models unnecessarly take away storage space.

You can use the cleanup script using `poetry run python src/cleanup.py`
to get rid off all the models in your `.cache` directory.

### 2. Preparing data

TBD

### 3. Executing inference

TBD

### 4. Calculating metrics

TBD

<!-- AUTHORS -->
## Authors

* **Tobias Stadler** - [devtobi](https://github.com/devtobi)

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE][license-url] for more information.

## Citation

If you reuse my work please cite my thesis as follows:

```bibtex
```

If you are interested in reading the thesis you can find it at [ADD TITLE](https://github.com/devtobi).

[license-shield]: https://img.shields.io/github/license/devtobi/aigelb.svg?style=for-the-badge&logo=github
[license-url]: https://github.com/devtobi/aigelb/blob/main/LICENSE

[commit-shield]: https://img.shields.io/github/last-commit/devtobi/cv?style=for-the-badge&logo=github
[commit-url]: https://github.com/devtobi/cv/commit/main
