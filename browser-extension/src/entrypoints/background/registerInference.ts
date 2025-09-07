import type { InferenceProgress } from "@/types/InferenceProgress.ts";

import { browser } from "wxt/browser";

import { streamResponse } from "@/api/ai.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

let currentAbortController: AbortController | null = null;
let trackedTabId: number | null = null;
let trackedGenerationId: string | null = null;

function resetInference() {
  trackedGenerationId = null;
  trackedTabId = null;
  currentAbortController = null;
}

function abortCurrentInference() {
  if (currentAbortController && !currentAbortController.signal.aborted) {
    currentAbortController.abort();
  }
}

export default function registerInference() {
  browser.tabs.onRemoved.addListener((tabId) => {
    if (tabId !== null && tabId === trackedTabId) {
      abortCurrentInference();
    }
  });

  onMessage("checkIsInferenceRunning", async () => {
    return !!trackedGenerationId;
  });

  onMessage("startInference", async (message) => {
    trackedTabId = message.sender.tab?.id as number;
    if (!trackedTabId || trackedGenerationId) return;
    currentAbortController = new AbortController();
    trackedGenerationId = message.data.generationId;
    try {
      await streamResponse(
        message.data.text,
        async (generatedText) => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              generationId: trackedGenerationId,
              status: "generating",
              text: generatedText,
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        },
        currentAbortController.signal,
        async () => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              generationId: trackedGenerationId,
              status: "completed",
              text: "",
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        },
        async () => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              generationId: trackedGenerationId,
              status: "completed",
              text: "",
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        },
        async () => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              generationId: trackedGenerationId,
              status: "error",
              text: "",
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        }
      );
    } catch {
      if (trackedTabId === null) return;
      await sendMessage(
        "inferenceProgress",
        {
          generationId: trackedGenerationId,
          text: "",
          status: "error",
        } as InferenceProgress,
        { tabId: trackedTabId }
      );
    } finally {
      resetInference();
    }
  });
  onMessage("abortInference", () => {
    abortCurrentInference();
  });
}
