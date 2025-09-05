<template>
  <v-app class="bg-transparent position-fixed w-100 h-100 bg-transparent">
    <selection-overlay
      v-model="selectionEnabled"
      @element-selected="onElementSelected"
    />
  </v-app>
</template>

<script setup lang="ts">
import type { RemoveListenerCallback } from "@webext-core/messaging";

import { onBeforeUnmount, onMounted, ref } from "vue";

import SelectionOverlay from "@/components/content/SelectionOverlay.vue";
import { onMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();

const selectionEnabled = ref<boolean>(false);
const selectedElement = ref<HTMLElement>();

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
