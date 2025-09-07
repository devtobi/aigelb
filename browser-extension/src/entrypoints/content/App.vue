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
  LINEARIZATION_FLEX_REGEX,
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

interface Run {
  nodes: Text[];
  i: number;
  pending: string;
  startedReplacing: boolean;
}
const currentRun = ref<Run | null>(null);

onMounted(() => {
  removeSelectionListener.value = onMessage("startSelection", () => {
    selectionEnabled.value = true;
  });
  removeInferenceListener.value = onMessage("inferenceProgress", (progress) => {
    const { generationId: gid, status, text } = progress.data;
    if (!selectedElement.value || gid !== generationId.value) return;

    if (status === "completed" || status === "error") {
      finalizeRun();
      return;
    }

    if (!currentRun.value) return;
    // Defer clearing original content until first generated chunk arrives
    if (!currentRun.value.startedReplacing) {
      for (const n of currentRun.value.nodes) n.nodeValue = "";
      currentRun.value.startedReplacing = true;
    }
    currentRun.value.pending += text;
    processCompleteMarkers();
    flushSafeTail();
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

    // Prepare run state; do not clear nodes yet. We wait for first LLM chunk.
    currentRun.value = {
      nodes: textNodes,
      i: 0,
      pending: "",
      startedReplacing: false,
    };

    await sendMessage("startInference", {
      generationId: generationId.value,
      text: linearized,
    });
  }
);

function resetState() {
  currentRun.value = null;
  generationId.value = "";
  selectedElement.value = null;
}

function appendToNodeByIndex(idx: number, text: string) {
  if (!text) return;
  const node = currentRun.value?.nodes[idx];
  if (node) node.nodeValue = (node.nodeValue ?? "") + text;
}

function appendToCurrentNode(text: string) {
  if (!currentRun.value) return;
  appendToNodeByIndex(currentRun.value.i, text);
}

function processCompleteMarkers() {
  if (!currentRun.value) return;
  while (true) {
    // check if marker found in generated content
    LINEARIZATION_FLEX_REGEX.lastIndex = 0;
    const m = LINEARIZATION_FLEX_REGEX.exec(currentRun.value.pending);
    if (!m) break;

    // update DOM content of specific text node
    const before = currentRun.value.pending.slice(0, m.index);
    const markerIdx = Number(m[1]);
    if (before) appendToNodeByIndex(markerIdx, before);

    // remove from pending content and go to next node (if available)
    currentRun.value.pending = currentRun.value.pending.slice(
      m.index + m[0].length
    );
    currentRun.value.i = markerIdx + 1;
    if (currentRun.value.i >= currentRun.value.nodes.length) {
      currentRun.value.pending = "";
      break;
    }
  }
}

function flushSafeTail() {
  if (!currentRun.value?.pending) return;
  const buf = currentRun.value.pending;
  const lastOpen = buf.lastIndexOf("⟦");
  const safeLen =
    lastOpen !== -1 && buf.indexOf("⟧", lastOpen) === -1
      ? lastOpen
      : buf.length;
  if (safeLen <= 0) return;

  const chunk = stripAllMarkers(buf.slice(0, safeLen));
  appendToCurrentNode(chunk);
  currentRun.value.pending = buf.slice(safeLen);
}

function finalizeRun() {
  if (currentRun.value?.pending) {
    processCompleteMarkers();
    if (currentRun.value.pending) {
      const leftover = stripAllMarkers(currentRun.value.pending);
      appendToCurrentNode(leftover);
      currentRun.value.pending = "";
    }
  }
  resetState();
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
