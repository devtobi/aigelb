<template>
  <div class="w-100">
    <v-tooltip
      v-if="isDisabled"
      activator="parent"
      location="bottom"
    >
      {{ disabledTooltip }}
    </v-tooltip>
    <v-btn
      @click="startSelection"
      size="large"
      block
      :color="isDisabled ? 'grey' : 'warning'"
      :prepend-icon="mdiCursorDefault"
      :disabled="isDisabled"
      :loading="inferenceRunning"
    >
      {{ i18n.t("popup.selectionButton.text") }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { mdiCursorDefault } from "@mdi/js";
import { i18n } from "#i18n";
import { computed, onMounted, ref } from "vue";

import { useModelAvailability } from "@/composables/useModelAvailability.ts";
import { useOllama } from "@/composables/useOllama.ts";
import {
  clearErrorBadge,
  closeWindow,
  getActiveTabId,
  setErrorBadge,
} from "@/utility/browser.ts";
import { sendMessage } from "@/utility/messaging.ts";

const { isOllamaAvailable, checkOllamaConnection } = useOllama();
const { isModelAvailable, checkModelAvailable } = useModelAvailability();

onMounted(async () => {
  await checkCondition();
  inferenceRunning.value = await sendMessage("checkIsInferenceRunning");
});

async function checkCondition() {
  await Promise.all([checkOllamaConnection(), checkModelAvailable()]);
  if (isDisabledByAvailability.value) {
    await setErrorBadge();
  } else {
    await clearErrorBadge();
  }
}

const inferenceRunning = ref<boolean>(false);
const isDisabledByAvailability = computed(() =>
  isOllamaAvailable.value !== true || isModelAvailable.value !== true
);
const isDisabled = computed(() => inferenceRunning.value || isDisabledByAvailability.value);

const disabledTooltip = computed(() => {
  if (isOllamaAvailable.value === false) {
    return i18n.t("popup.selectionButton.tooltip.ollamaUnavailable");
  }
  if (isModelAvailable.value === false) {
    return i18n.t("popup.selectionButton.tooltip.modelUnavailable");
  }
  if (inferenceRunning.value === true) {
    return i18n.t("popup.selectionButton.tooltip.inferenceRunning");
  }
  return null;
});

async function startSelection() {
  await checkCondition();
  if (!isDisabled.value) {
    const tabId = await getActiveTabId();
    if (tabId) {
      await sendMessage("startSelection", undefined, { tabId });
      closeWindow();
    }
  }
}
</script>
