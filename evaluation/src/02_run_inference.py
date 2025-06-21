from os import getenv
from typing import cast

from llama_cpp import (
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
    CreateChatCompletionResponse,
    Llama,
)

from utility import ConfigurationService, LoggingService

# Check CPU / GPU mode
ConfigurationService.load_environment_configuration()
use_cpu: bool = getenv("USE_CPU") == "True"
gpu_layers: int = 0 if use_cpu else -1

LoggingService.mute_llamacpp_logging()

# load model
llm: Llama = Llama.from_pretrained(
    "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
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
