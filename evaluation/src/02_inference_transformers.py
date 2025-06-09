from os import getenv
from sys import exit
from typing import cast

from dotenv import load_dotenv
from huggingface_hub.errors import LocalEntryNotFoundError
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Pipeline,
    PreTrainedModel,
    PreTrainedTokenizer,
    pipeline,
)

# Check CPU / GPU mode
load_dotenv()
use_cpu = getenv("USE_CPU") or "True"

# load model
try:
    tokenizer: PreTrainedTokenizer = cast(PreTrainedTokenizer, AutoTokenizer.from_pretrained(
        "Qwen/Qwen2.5-0.5B-Instruct", local_files_only=True
    ))
    model: PreTrainedModel = cast(PreTrainedModel, AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2.5-0.5B-Instruct", local_files_only=True
    ))
except (LocalEntryNotFoundError, OSError) as e:
    print(e)
    exit(0)

# execute inference
if use_cpu:
    generate: Pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device="cpu",
    )
else:
    generate: Pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
response = generate("Hello, I'm a language model")
print(response)
