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
import { onMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();

const selectionEnabled = ref<boolean>(false);
const selectedElement = ref<HTMLElement | null>(null);

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    selectionEnabled.value = true;
  });
});

onBeforeUnmount(() => {
  if (removeSelectionListener.value) {
    removeSelectionListener.value();
  }
});

function onElementSelected(element: HTMLElement) {
  selectionEnabled.value = false;
  selectedElement.value = element;
}

watch(
  () => selectedElement.value,
  (selectedElement) => {
    if (!selectedElement) return;
    console.debug(selectedElement);
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
