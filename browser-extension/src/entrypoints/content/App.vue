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
import {
  LINEARIZATION_REGEX,
  linearizeTextNodesForInference,
} from "@/utility/conversion.ts";
import { collectTextNodes } from "@/utility/dom.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();
const removeInferenceListener = ref<RemoveListenerCallback>();

const selectionEnabled = ref<boolean>(false);
const selectedElement = ref<HTMLElement | null>(null);

const generationId = ref<string>("");

type Run = { nodes: Text[]; i: number; pending: string };
const runs = new Map<string, Run>();

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    selectionEnabled.value = true;
  });
  removeInferenceListener.value = onMessage("inferenceProgress", (progress) => {
    const { generationId: gid, status, text } = progress.data;
    if (!selectedElement.value || gid !== generationId.value) return;

    if (status === "completed" || status === "error") {
      runs.delete(gid);
      generationId.value = "";
      selectedElement.value = null;
      return;
    }

    // Streamed delta handling
    const run = runs.get(gid);
    if (!run) return;
    run.pending += text;

    while (true) {
      LINEARIZATION_REGEX.lastIndex = 0;
      const m = LINEARIZATION_REGEX.exec(run.pending);
      // marker not reached
      if (!m) {
        const node = run.nodes[run.i];
        if (!node) return;
        node.nodeValue = (node.nodeValue ?? "") + run.pending;
        run.pending = "";
        break;
      }

      const chunk = run.pending.slice(0, m.index);
      const node = run.nodes[run.i];
      if (node && chunk) node.nodeValue = (node.nodeValue ?? "") + chunk;

      run.i += 1; // advance to next node
      run.pending = run.pending.slice(m.index + m[0].length); // drop marker

      if (run.i >= run.nodes.length) {
        run.pending = "";
        break;
      }
    }
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

    // Prepare run state and clear existing node content for replacement
    runs.set(generationId.value, { nodes: textNodes, i: 0, pending: "" });
    for (const n of textNodes) n.nodeValue = "";

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
