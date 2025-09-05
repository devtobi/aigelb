import type { SystemModelMessage, UserModelMessage } from "ai";

import {
  simulateStreamingMiddleware,
  smoothStream,
  streamText,
  wrapLanguageModel,
} from "ai";
import { ollama } from "ai-sdk-ollama/browser";

import {
  LLM_HUGGINGFACE_FILE,
  LLM_HUGGINGFACE_REPO,
  LLM_SUPPORT_STREAMING,
  SYSTEM_PROMPT,
  USER_PROMPT_TEMPLATE,
} from "@/config.ts";
import { convertToOllamaUrl } from "@/utility/conversion.ts";

function stream(
  model: string,
  supportsStreaming: boolean,
  prompt: string,
  systemPrompt: string,
  abortSignal?: AbortSignal,
  onFinish?: () => void,
  onAbort?: () => void,
  onError?: () => void
) {
  const { textStream } = streamText({
    model: supportsStreaming
      ? ollama(model)
      : wrapLanguageModel({
          model: ollama(model),
          middleware: simulateStreamingMiddleware(),
        }),
    messages: [
      {
        role: "system",
        content: systemPrompt,
      } as SystemModelMessage,
      {
        role: "user",
        content: prompt,
      } as UserModelMessage,
    ],
    maxRetries: 0,
    abortSignal,
    onFinish,
    onAbort,
    onError,
    experimental_transform: smoothStream(),
  });
  return textStream;
}

export async function streamResponse(
  text: string,
  onPartialGeneration: (part: string) => void,
  abortSignal?: AbortSignal,
  onFinish?: () => void,
  onAbort?: () => void,
  onError?: () => void
) {
  const model = convertToOllamaUrl(LLM_HUGGINGFACE_REPO, LLM_HUGGINGFACE_FILE);
  const userPrompt = USER_PROMPT_TEMPLATE.replace("{source}", text);

  const textStream = stream(
    model,
    LLM_SUPPORT_STREAMING,
    userPrompt,
    SYSTEM_PROMPT,
    abortSignal,
    onFinish,
    onAbort,
    onError
  );

  let response = "";
  try {
    for await (const textPart of textStream) {
      response += textPart;
      onPartialGeneration(response);
    }
  } catch (error) {
    if (!abortSignal?.aborted) {
      throw error;
    }
  }
}
