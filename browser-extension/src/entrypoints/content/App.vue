<template>
  <v-app> </v-app>
</template>

<script setup lang="ts">
import type { RemoveListenerCallback } from "@webext-core/messaging";

import { onBeforeUnmount, onMounted, ref } from "vue";

import { onMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () =>
    console.debug("startSelection")
  );
});

onBeforeUnmount(() => {
  if (removeSelectionListener.value) {
    removeSelectionListener.value();
  }
});
</script>
