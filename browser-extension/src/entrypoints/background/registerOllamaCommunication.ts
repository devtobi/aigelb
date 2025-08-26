import { onMessage } from "@/utility/messaging.ts";
import { isAvailable, isModelAvailable } from "@/api/ollama.ts";

export default function registerOllamaCommunication() {
  onMessage("checkOllamaConnection", async () => {
    return await isAvailable();
  });
  onMessage("checkIsModelAvailable", async (message) => {
    return await isModelAvailable(message.data);
  });
}
