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
      @click="() => (!inferenceRunning ? startSelection() : abortInference())"
      size="large"
      block
      :color="isDisabled ? 'grey' : 'warning'"
      :prepend-icon="!inferenceRunning ? mdiCursorDefault : mdiClose"
      :text="
        !inferenceRunning
          ? i18n.t('popup.selectionButton.startText')
          : i18n.t('popup.selectionButton.stopText')
      "
      :disabled="isDisabled"
    />
  </div>
</template>

<script setup lang="ts">
import { mdiClose, mdiCursorDefault } from "@mdi/js";
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
  if (isDisabled.value) {
    await setErrorBadge();
  } else {
    await clearErrorBadge();
  }
}

const inferenceRunning = ref<boolean>(false);
const isDisabled = computed(
  () => isOllamaAvailable.value !== true || isModelAvailable.value !== true
);

const disabledTooltip = computed(() => {
  if (isOllamaAvailable.value === false) {
    return i18n.t("popup.selectionButton.tooltip.ollamaUnavailable");
  }
  if (isModelAvailable.value === false) {
    return i18n.t("popup.selectionButton.tooltip.modelUnavailable");
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

async function abortInference() {
  if (inferenceRunning.value) {
    await sendMessage("abortInference");
    closeWindow();
  }
}
</script>
