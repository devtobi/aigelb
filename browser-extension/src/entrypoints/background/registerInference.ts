import { streamResponse } from "@/api/ai.ts";
import { onMessage } from "@/utility/messaging.ts";

export default function registerInference() {
  let inferenceRunning = true;

  function setInferenceRunning(isRunning: boolean) {
    if (inferenceRunning === isRunning) return;
    inferenceRunning = isRunning;
  }

  onMessage("checkIsInferenceRunning", async () => {
    return inferenceRunning;
  });

  onMessage("startInference", async (message) => {
    if (inferenceRunning) return;
    const text = message.data;
    const abortController = new AbortController();
    setInferenceRunning(true);
    try {
      await streamResponse(
        text,
        () => {
          // In the future, partial results can be forwarded to the content script.
        },
        abortController.signal,
        () => setInferenceRunning(false),
        () => setInferenceRunning(false),
        () => setInferenceRunning(false)
      );
    } catch {
      setInferenceRunning(false);
    } finally {
      setInferenceRunning(false);
    }
  });
}
