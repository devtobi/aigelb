from ctypes import CFUNCTYPE, c_char_p, c_int, c_void_p
from os import getenv

from dotenv import load_dotenv
from llama_cpp import Llama, llama_log_set

from helper import get_model_cache_dir


# Mute logging for verbose llama-cpp output
def my_log_callback(level, message, user_data):
    pass


log_callback = CFUNCTYPE(None, c_int, c_char_p, c_void_p)(my_log_callback)
llama_log_set(log_callback, c_void_p())

# Check CPU / GPU mode
load_dotenv()
use_cpu = getenv("USE_CPU")
gpu_layers = 0 if use_cpu == "True" else -1

# load model
model_cache_dir = get_model_cache_dir()
llm = Llama.from_pretrained(
    "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    cache_dir=model_cache_dir,
    local_files_only=True,
    verbose=False,
    n_gpu_layers=gpu_layers,
)

# execute inference
completion_response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are an that always uses capital words."},
        {"role": "user", "content": "Tell me a little story about bees."},
    ],
    max_tokens=1000,
)

content = completion_response
print(content)
