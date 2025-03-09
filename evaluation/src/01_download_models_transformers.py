from transformers import AutoModelForCausalLM, AutoTokenizer

from helper import get_model_cache_dir

model_cache_dir = get_model_cache_dir()

# downloading models
AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", cache_dir=model_cache_dir)
AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct", cache_dir=model_cache_dir
)
