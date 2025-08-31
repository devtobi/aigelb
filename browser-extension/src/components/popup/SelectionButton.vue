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
      color="warning"
      :prepend-icon="mdiCursorDefault"
      :disabled="isDisabled"
    >
      {{ i18n.t("popup.selectionButton.text") }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { mdiCursorDefault } from "@mdi/js";
import { i18n } from "#i18n";
import { computed, onMounted } from "vue";

import { useModelAvailability } from "@/composables/useModelAvailability.ts";
import { useOllama } from "@/composables/useOllama.ts";
import { getActiveTabId } from "@/utility/browser.ts";
import { sendMessage } from "@/utility/messaging.ts";

const { isOllamaAvailable, checkOllamaConnection } = useOllama();
const { isModelAvailable, checkModelAvailable } = useModelAvailability();

onMounted(async () => {
  await checkCondition();
});

async function checkCondition() {
  await Promise.all([checkOllamaConnection(), checkModelAvailable()]);
}

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
    }
  }
}
</script>
