import { streamResponse } from "@/api/ai.ts";
import { onMessage } from "@/utility/messaging.ts";

let currentAbortController: AbortController | null = null;
let inferenceRunning = true;

function setInferenceRunning(isRunning: boolean) {
  if (inferenceRunning === isRunning) return;
  inferenceRunning = isRunning;
}

export default function registerInference() {
  onMessage("checkIsInferenceRunning", async () => {
    return inferenceRunning;
  });

  onMessage("startInference", async (message) => {
    if (inferenceRunning) return;
    const text = message.data;
    currentAbortController = new AbortController();
    setInferenceRunning(true);
    try {
      await streamResponse(
        text,
        () => {
          // In the future, partial results can be forwarded to the content script.
        },
        currentAbortController.signal,
        () => setInferenceRunning(false),
        () => setInferenceRunning(false),
        () => setInferenceRunning(false)
      );
    } catch {
      setInferenceRunning(false);
    } finally {
      setInferenceRunning(false);
      currentAbortController = null;
    }
  });

  onMessage("abortInference", async () => {
    if (currentAbortController && !currentAbortController.signal.aborted) {
      currentAbortController.abort();
    }
    setInferenceRunning(false);
    currentAbortController = null;
  });
}
