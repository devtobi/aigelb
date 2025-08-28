import { ref } from "vue";

import { sendMessage } from "@/utility/messaging.ts";

export function useOllama() {
  const isOllamaAvailable = ref<boolean | undefined>(undefined);

  async function checkOllamaConnection(): Promise<boolean> {
    isOllamaAvailable.value = await sendMessage("checkOllamaConnection");
    return isOllamaAvailable.value === true;
  }

  return { isOllamaAvailable, checkOllamaConnection };
}
