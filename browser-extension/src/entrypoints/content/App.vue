<template>
  <v-app class="bg-transparent position-fixed w-100 h-100 bg-transparent">
    <selection-overlay v-model="enabled" />
  </v-app>
</template>

<script setup lang="ts">
import type { RemoveListenerCallback } from "@webext-core/messaging";

import { onBeforeUnmount, onMounted, ref } from "vue";

import SelectionOverlay from "@/components/content/SelectionOverlay.vue";
import { onMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();

const enabled = ref<boolean>(false);

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    enabled.value = true;
  });
});

onBeforeUnmount(() => {
  if (removeSelectionListener.value) {
    removeSelectionListener.value();
  }
});
</script>

<style>
html,
body {
  margin: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
