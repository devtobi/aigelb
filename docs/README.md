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

* Programming language: [Python](https://www.python.org)
* Package management: [uv](https://docs.astral.sh/uv/)
* Model downloads: [HuggingFace Hub](https://huggingface.co)
* LLM inference: [llama-cpp-python](https://llama-cpp-python.readthedocs.io)
* Evaluation metrics:
  * Machine translation: [HuggingFace Evaluate](https://huggingface.co/docs/evaluate/index)
  * Text readability: [TextStat](https://textstat.org)
  * Lexical diversity: [LexicalRichness](https://lexicalrichness.readthedocs.io/en/latest/)

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
* uv as dependency management tool

installed on your system.
Please check out the [Python documentation](https://www.python.org/downloads)
and [uv documentation](https://docs.astral.sh/uv/getting-started/installation/)
for installation instructions.

The exact compatible version of Python
can be found in the `pyproject.toml` file inside the `evaluation` directory.

When the requirements above are met,
you only need to execute `uv sync` inside the `evaluation` directory
to setup the virtual environment and download the required packages.

**Note:** To make inference and hardware acceleration work on your machine, you might have to do additional steps to use the proper backend for your architecture and platform in `llama-cpp-python`. You can pass required environment variables like `CMAKE_ARGS` directly to `uv sync`. E.g. for installing on Apple silicon using Metal acceleration execute `CMAKE_ARGS="-DGGML_METAL=on" uv sync`.
See [official documentation](https://llama-cpp-python.readthedocs.io/en/latest/#supported-backends)
for further information and up-to-date instructions.

### Usage

All mentioned scripts can be run via uv
using the following command: `uv run <script-path>.py`

The files inside the `config` directory
allow further customization of the behaviour
and will be further explained in the sections below.

### 1. Downloading models

#### Configuration

You can define which models you want to download
inside the `models.csv` file in the `evaluation` directory.
You can only use [GGUF](https://huggingface.co/docs/hub/gguf)-based models from the [HuggingFace](https://huggingface.co) platform.

The file has the following columns:

* `_repo_id`: repository name of the model (e.g. [bartowski/Llama-3.2-3B-Instruct-GGUF](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF)).
* `_gguf_filename`: filename to select the variant of the model for different quantizations (e.g. [Llama-3.2-3B-Instruct-Q5_K_M.gguf](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/blob/main/Llama-3.2-3B-Instruct-Q5_K_M.gguf))
* `_gated`: `True` or `False` whether the model is gated
(e.g. when a license agreement consent on HuggingFace
platform is necessary for your account).

Relevant environment variables for the `config.env` file are the following:

* `HF_TOKEN` (optional): HuggingFace token for your account
to fetch gated models you have access to on the platform.
See [HuggingFace documentation](https://huggingface.co/docs/hub/security-tokens)
for further information.
* `HF_HOME` (optional): Custom directory to store cache files and models downloaded for evaluation. If not set, will use default directory `~/.cache/huggingface`

#### Execution

To download the models you selected for evaluation,
you need to run the download script
using `uv run src/01_download_models.py`
when you are inside the `evaluation` directory.

The script will read the content of the `models.csv` file
and ask you to confirm the download before starting.

The downloaded models will be stored to the configured cache directory folder for later use.

**Tip:** If you interrupt the model downloads by quitting the script execution,
the script will automatically resume the downloads where they stopped.

#### Clean up

When you experiment with different models
your cache folder might fill up quickly
and unused models unnecessarly take away storage space.

You can use the cleanup script using `uv run python src/cleanup.py`
to get rid off all the models in your cache directory.

**Warning:** If you did not set a custom cache directory, this will remove all the models you ever downloaded from the HuggingFace platform, even from other projects.

### 2. Preparing data

TBD

### 3. Running inference

#### Configuration

##### Source data

The source data can be configured in the `data/sources.csv` file. Each row in that file will be a sentence that is being passed to the LLM in the configured user prompt.

**Important**: The entries must be quoted using double quotes to not interpret `,` inside the source sentences as a column separator.

##### System prompt

The system prompt can be configured inside the `config/system_prompt.txt` file. Usally the role of the LLM as well as instructions are defined here. One can also include examples to guide the LLM using in-context-learning.

##### User prompt

The user prompt can be configured in the `config/user_prompt.txt` file. It contains the specific task as hand (e.g. translating a specific sentence into plain language).

**Important**: The user prompt must contain `{source}` to insert the specific source sentence into the user prompt at LLM inferene time.

##### Inference

Relevant environment variables for the `config.env` are the following:

* `USE_CPU` (optional): `True` or `False` whether CPU or GPU should be used for LLM inference. If not set, will use GPU.
* `NUM_THREADS` (optional): Number of threads to use when running CPU inference. If not set, will be automatically inferred based on system capabilities
* `CONTEXT_LENGTH` (optional): Context length to use for inference, can speed up performance when decreased, needs to be bug enough for prompt tokens to fit. If not set, will infer the context length from the given model.
* `STRUCTURED_OUTPUT_KEY` (optional): Key for the JSON object to expect from LLM generation used to improve LLM generation via Structured Output, not part of the final result. If not set `result` will be used as key.
* `TEMPERATURE` (optional): Temperature to use for model inference for controlling creativity. If not set `0.2` will be used.

#### Execution

To run the LLM inference,
you need to run the inference script
using `uv run src/02_run_inference.py`
when you are inside the `evaluation` directory.

The script will read the content of `sources.csv`, `system_prompt.csv`, `user_prompt.csv` and `models.csv` and ask for confirmation before starting inference.

The script will sequentially load the configured models and use each configured source sentence in an isolated inference execution.
The results are stored in the `results` folder inside a directory named by the timestamp of generation start. Inside will be a `.csv`file for each used model.

**Tip**: Depending on the amount of models, the amount of configured sentences and the capabilities of the system this task can take from a few minutes to a couple of days.
Thus a lockfile mechanism has been implemented that allows for interrupting and later on resuming the inference task. A lockfile named `timestamp.lock` will be placed in the `predictions` folder in this case.

### 4. Calculating metrics

#### Configuration

##### Metrics

You can define which metrics you want to evaluate using the `metrics.csv` file.
The file has the following columns:

* `_name`: name of the metric to calculate, can be any method of the integrated libraries ([HuggingFace Evaluate](https://huggingface.co/docs/evaluate/index), [TextStat](https://textstat.org) or [LexicalRichness](https://lexicalrichness.readthedocs.io/en/latest/))
* `_kwargs` (optional): Passes additional arguments as a python dictionary to the metric function (check the official docs of the specified metric for more information), must be in the form `"{'parameter': value}"`

**Note**: A special argument in the dictionary is `target`. Because some metrics calculate the results as a dictionary, the `target` argument is required to specify which value of the dictionary to extract. Please check the library documentations for information about method outputs.

Examples:
* `wiener_sachtextformel,"{'variant': 1}"` calculates `wiener_sachtextformel` from TextStat using `variant: 1`
* `ttr` calculates `ttr` from LexicalRichness without any additional configuration
* `bertscore,"{'lang': 'de', 'target': 'f1'}` calculates  `bertscore` from HuggingFace Evaluate using `lang: 'de'` and extracting `f1`from the calculated output dictionary

**Note**: Often setting additional arguments is required for specific metrics, as otherwise no calculation is possible. Check the documentation of the libraries.

**Important**: When using metrics from the [HuggingFace Evaluate](https://huggingface.co/docs/evaluate/index) library, often times additional packages are necessary, e.g. to use `bertscore` the package `bert-score` must be installed.
This can be done via `uv pip install <package-name>`.

##### References

Metrics from the Machine Translation field require a (gold standard) reference to compare to in order to be calculated. The references can be configured in the `references.csv` file. Each row in that file will be a sentence that is being compared to the generated sentence in the model-specific file of the `predictions` directory.

**Important**: If the sentence contains special characters or commas, the sentences need to be double-quoted, as otherwise those commas will be interpreted as column separators.

#### Execution

To calculate the metrics you selected,
you need to run the calculation script
using `uv run src/03_calculate_metrics.py`
when you are inside the `evaluation` directory.

The script will read the content of the `models.csv` and `metrics.csv` file
and ask you to confirm the configured models and metrics to use for calculation.

The predictions used for calculation will always be taken from the latest folder inside the `predictions` directory.
The results will be stored in the `results` directory inside a folder named after the generation timestamp as `.csv` files containing the timestamp of metric calculation (`results/<timestamp-generation>/<timestamp-calculation>.csv`). The result file contains:
1. Results based on reference-free metrics for the input data
2. Results based on reference-free metrics for the reference data
3. Results based on all metrics for each model-generated data

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
