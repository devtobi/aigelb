import { computed, ref } from "vue";

import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config/config.ts";
import { convertToOllamaUrl } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

export function useModelAvailability() {
  const isModelAvailable = ref<boolean | undefined>(undefined);

  const ollamaPullUrl = computed(() =>
    convertToOllamaUrl(LLM_HUGGINGFACE_REPO, LLM_HUGGINGFACE_FILE)
  );

  async function checkModelAvailable(): Promise<boolean> {
    isModelAvailable.value = await sendMessage(
      "checkIsModelAvailable",
      ollamaPullUrl.value
    );
    return isModelAvailable.value === true;
  }

  return { isModelAvailable, checkModelAvailable };
}
