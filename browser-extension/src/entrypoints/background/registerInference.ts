import type { InferenceProgress } from "@/types/InferenceProgress.ts";

import { browser } from "wxt/browser";

import { streamResponse } from "@/api/ai.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

let currentAbortController: AbortController | null = null;
let inferenceRunning = false;
let trackedTabId: number | null = null;

function abortCurrentInference() {
  if (currentAbortController && !currentAbortController.signal.aborted) {
    currentAbortController.abort();
  }
  inferenceRunning = false;
  currentAbortController = null;
  trackedTabId = null;
}

export default function registerInference() {
  browser.tabs.onRemoved.addListener((tabId) => {
    if (tabId !== null && tabId === trackedTabId) {
      abortCurrentInference();
    }
  });

  onMessage("checkIsInferenceRunning", async () => {
    return inferenceRunning;
  });

  onMessage("startInference", async (message) => {
    if (inferenceRunning) return;
    trackedTabId = message.data.tabId;
    currentAbortController = new AbortController();
    inferenceRunning = true;
    try {
      await streamResponse(
        message.data.text,
        async (generatedText) => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              text: generatedText,
              status: "generating",
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
              text: "",
              status: "completed",
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        },
        async () => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              text: "",
              status: "completed",
            } as InferenceProgress,
            { tabId: trackedTabId }
          );
        },
        async () => {
          if (trackedTabId === null) return;
          await sendMessage(
            "inferenceProgress",
            {
              text: "",
              status: "error",
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
          text: "",
          status: "error",
        } as InferenceProgress,
        { tabId: trackedTabId }
      );
    } finally {
      abortCurrentInference();
    }
  });

  onMessage("abortInference", async () => {
    abortCurrentInference();
  });
}
