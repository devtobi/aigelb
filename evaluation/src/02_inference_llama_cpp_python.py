from ctypes import CFUNCTYPE, c_char_p, c_int, c_void_p
from os import getenv
from typing import cast

from dotenv import load_dotenv
from llama_cpp import (
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
    CreateChatCompletionResponse,
    Llama,
    llama_log_set,
)

from helper import get_model_cache_dir


# Mute logging for verbose llama-cpp output, no type information required
def my_log_callback(level, message, user_data):
    pass


log_callback = CFUNCTYPE(None, c_int, c_char_p, c_void_p)(my_log_callback)
# pyrefly: ignore
llama_log_set(log_callback, c_void_p())

# Check CPU / GPU mode
load_dotenv()
use_cpu: str = getenv("USE_CPU") or "True"
gpu_layers: int = 0 if use_cpu == "True" else -1

# load model
model_cache_dir: str = get_model_cache_dir()
llm: Llama = Llama.from_pretrained(
    "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    cache_dir=model_cache_dir,
    local_files_only=True,
    verbose=False,
    n_gpu_layers=gpu_layers,
)

# execute inference
system_message: ChatCompletionRequestSystemMessage = { "role": "system", "content": "You are an AI that always uses capital words when responding." }
user_message: ChatCompletionRequestUserMessage = { "role": "user", "content": "Tell me a little story about bees." }
completion_response: CreateChatCompletionResponse = cast(CreateChatCompletionResponse, llm.create_chat_completion(
    messages=[system_message, user_message],
    max_tokens=1000,
))

content: CreateChatCompletionResponse = completion_response
print(content)
