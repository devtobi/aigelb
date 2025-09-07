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
  LINEARIZATION_PREFIX,
  LINEARIZATION_SUFFIX,
  linearizeTextNodesForInference,
  stripAllMarkers,
} from "@/utility/conversion.ts";
import { collectTextNodes } from "@/utility/dom.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

const removeSelectionListener = ref<RemoveListenerCallback>();
const removeInferenceListener = ref<RemoveListenerCallback>();

const selectionEnabled = ref<boolean>(false);
const selectedElement = ref<HTMLElement | null>(null);

const generationId = ref<string>("");

type Run = { nodes: Text[]; i: number; pending: string };
const currentRun = ref<Run | null>(null);

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    selectionEnabled.value = true;
  });
  removeInferenceListener.value = onMessage("inferenceProgress", (progress) => {
    const { generationId: gid, status, text } = progress.data;
    if (!selectedElement.value || gid !== generationId.value) return;

    if (status === "completed" || status === "error") {
      // On completion, flush any remaining buffer safely and strip markers
      if (currentRun.value && currentRun.value.pending) {
        // Process any final complete markers
        while (true) {
          LINEARIZATION_REGEX.lastIndex = 0;
          const m = LINEARIZATION_REGEX.exec(currentRun.value.pending);
          if (!m) break;

          const before = currentRun.value.pending.slice(0, m.index);
          const markerIdx = Number(m[1]);
          const target = currentRun.value.nodes[markerIdx];
          if (target && before) target.nodeValue = (target.nodeValue ?? "") + before;
          currentRun.value.pending = currentRun.value.pending.slice(m.index + m[0].length);
          currentRun.value.i = markerIdx + 1;
        }
        // Append any leftovers (with markers stripped) to current node
        if (currentRun.value.pending) {
          const node = currentRun.value.nodes[currentRun.value.i];
          const chunk = stripAllMarkers(currentRun.value.pending);
          if (node) node.nodeValue = (node.nodeValue ?? "") + chunk;
          currentRun.value.pending = "";
        }
      }

      currentRun.value = null;
      generationId.value = "";
      selectedElement.value = null;
      return;
    }

    // Streamed delta handling
    if (!currentRun.value) return;
    currentRun.value.pending += text;

    // Process all complete segments in the buffer using explicit marker indices
    while (true) {
      LINEARIZATION_REGEX.lastIndex = 0;
      const m = LINEARIZATION_REGEX.exec(currentRun.value.pending);
      if (!m) break; // no full segment boundary in buffer yet

      const before = currentRun.value.pending.slice(0, m.index);
      const markerIdx = Number(m[1]);

      const target = currentRun.value.nodes[markerIdx];
      if (target && before) {
        target.nodeValue = (target.nodeValue ?? "") + before;
      }

      // Drop processed content + marker from buffer and set current index to the next node
      currentRun.value.pending = currentRun.value.pending.slice(m.index + m[0].length);
      currentRun.value.i = markerIdx + 1;

      if (currentRun.value.i >= currentRun.value.nodes.length) {
        // We've reached/passed the last node; discard any trailing buffer until more arrives
        currentRun.value.pending = "";
        break;
      }
    }

    // Safely stream whatever remains towards the current target index.
    // Keep any possible partial marker at the end of the buffer to avoid breaking markers across chunks.
    if (currentRun.value.pending) {
      // Find the last possible start of a marker (be tolerant: look for the opening bracket only)
      const lastOpenPos = currentRun.value.pending.lastIndexOf("⟦");
      let safeLen = currentRun.value.pending.length;
      if (lastOpenPos !== -1) {
        // If there is no closing suffix after the last opening, keep the trailing part (potential partial marker) in the buffer
        const hasClosing = currentRun.value.pending.indexOf("⟧", lastOpenPos) !== -1;
        if (!hasClosing) {
          safeLen = lastOpenPos;
        }
      }

      if (safeLen > 0) {
        const node = currentRun.value.nodes[currentRun.value.i];
        // Remove any internal complete markers that might have slipped through
        const chunk = stripAllMarkers(currentRun.value.pending.slice(0, safeLen));
        if (node && chunk) node.nodeValue = (node.nodeValue ?? "") + chunk;
        currentRun.value.pending = currentRun.value.pending.slice(safeLen);
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
    currentRun.value = { nodes: textNodes, i: 0, pending: "" };
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
