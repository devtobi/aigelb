from os import getenv

from dotenv import load_dotenv
from huggingface_hub.errors import LocalEntryNotFoundError
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from helper import get_model_cache_dir

model_cache_dir = get_model_cache_dir()

# Check CPU / GPU mode
load_dotenv()
use_cpu = getenv("USE_CPU") == "True"

# load model
try:
    tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen2.5-0.5B-Instruct", cache_dir=model_cache_dir, local_files_only=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2.5-0.5B-Instruct", cache_dir=model_cache_dir, local_files_only=True
    )
except (LocalEntryNotFoundError, OSError) as e:
    print(e)
    exit(1)

# execute inference
if use_cpu:
    generate = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device="cpu",
    )
else:
    generate = pipeline("text-generation", model=model, tokenizer=tokenizer)
response = generate("Hello, I'm a language model")
print(response)
