<template>
  <v-app class="bg-transparent position-fixed w-100 h-100 bg-transparent">
    <translation-overlay :element="selectedElement" />
    <selection-overlay
      v-model="selectionEnabled"
      @element-selected="onElementSelected"
    />
  </v-app>
</template>

<script setup lang="ts">
import type { RemoveListenerCallback } from "@webext-core/messaging";

import { onBeforeUnmount, onMounted, ref, watch } from "vue";

import SelectionOverlay from "@/components/content/SelectionOverlay.vue";
import TranslationOverlay from "@/components/content/TranslationOverlay.vue";
import { linearizeTextNodesForInference } from "@/utility/conversion.ts";
import { collectTextNodes } from "@/utility/dom.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();
const removeInferenceListener = ref<RemoveListenerCallback>();

const selectionEnabled = ref<boolean>(false);
const selectedElement = ref<HTMLElement | null>(null);

const generationId = ref<string>("");

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    selectionEnabled.value = true;
  });
  removeInferenceListener.value = onMessage("inferenceProgress", (progress) => {
    if (
      !selectedElement.value ||
      progress.data.generationId !== generationId.value
    )
      return;
    if (progress.data.status === "completed") {
      generationId.value = "";
      selectedElement.value = null;
      return;
    }
    console.debug(progress.data.text);
  });
});

onBeforeUnmount(() => {
  if (removeSelectionListener.value) {
    removeSelectionListener.value();
  }
  if (removeInferenceListener.value) {
    removeInferenceListener.value();
  }
});

function onElementSelected(element: HTMLElement) {
  selectionEnabled.value = false;
  selectedElement.value = element;
}

watch(
  () => selectedElement.value,
  async (newSelectedElement) => {
    if (!newSelectedElement) return;
    const textNodes = collectTextNodes(newSelectedElement);
    if (!textNodes.length) {
      selectedElement.value = null;
      return;
    }
    const linearized = linearizeTextNodesForInference(textNodes);
    generationId.value = crypto.randomUUID() as string;

    await sendMessage("startInference", {
      generationId: generationId.value,
      text: linearized,
    });
  }
);
</script>

<style>
html,
body {
  margin: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.v-application {
  z-index: 2147483647 !important;
}
</style>
