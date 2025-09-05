<template>
  <v-overlay
    :model-value="enabled"
    persistent
    :scrim="false"
    :absolute="false"
    contained
    content-class="selection-overlay-content"
  >
    <div
      ref="overlayUi"
      class="overlay-ui-root"
    >
      <v-sheet
        v-show="rect.visible"
        class="rect-overlay pointer-events-none position-fixed"
        :style="{
          left: rect.x + 'px',
          top: rect.y + 'px',
          width: rect.w + 'px',
          height: rect.h + 'px',
        }"
      />

      <v-alert
        v-if="enabled"
        color="orange"
        type="info"
        variant="elevated"
        class="pa-3 position-fixed description-alert"
        prominent
        closable
        :close-icon="mdiEyeOff"
        :title="i18n.t('content.selectionOverlay.title')"
        :text="i18n.t('content.selectionOverlay.description')"
      >
        <template #append>
          <v-btn
            variant="text"
            @click="enabled = false"
            size="small"
            :text="i18n.t('common.cancel')"
          />
        </template>
      </v-alert>
    </div>
  </v-overlay>
</template>

<script setup lang="ts">
import { mdiEyeOff } from "@mdi/js";
import { i18n } from "#i18n";
import {
  onBeforeUnmount,
  onMounted,
  reactive,
  ref,
  useTemplateRef,
  watch,
} from "vue";

import {
  elementAtClientPoint,
  elementContainsText, getXPathForElement,
  isInsideElement, replaceElementByXPath,
} from "@/utility/dom.ts";
import type { SelectionData } from "@/types/SelectionData.ts";

const enabled = defineModel<boolean>();

const rect = reactive({ x: 0, y: 0, w: 0, h: 0, visible: false });

const overlayUi = useTemplateRef<HTMLElement>("overlayUi");

function onMove(e: MouseEvent) {
  if (!enabled.value) return;
  if (isInsideElement(e, overlayUi.value)) {
    rect.visible = false;
    return;
  }
  const t = elementAtClientPoint(overlayUi.value, e.clientX, e.clientY);
  if (!t || t === document.documentElement || t === document.body) {
    rect.visible = false;
    return;
  }
  if (!elementContainsText(t)) {
    rect.visible = false;
    return;
  }
  const r = (t as Element).getBoundingClientRect();
  rect.x = Math.round(r.left);
  rect.y = Math.round(r.top);
  rect.w = Math.round(r.width);
  rect.h = Math.round(r.height);
  rect.visible = true;
}

function onClick(e: MouseEvent) {
  if (!enabled.value || isInsideElement(e, overlayUi.value)) return;
  const t = elementAtClientPoint(overlayUi.value, e.clientX, e.clientY);
  if (!t || !elementContainsText(t)) return;

  e.preventDefault();
  e.stopPropagation();

  const selectionData: SelectionData = {
    content: (t as HTMLElement).innerHTML,
    xPath: getXPathForElement(t)
  }
  console.debug("selectionData:", selectionData);
  // TODO START ASYNCHRONOUS TRANSLATION EVENT
  // DUMMY TESTING TO REPLACE DOM CONTENT
  replaceElementByXPath(selectionData.xPath, document.createTextNode("Übersetzen ist aktuell noch nicht möglich!"))

  enabled.value = false;
}

function onKeyDown(e: KeyboardEvent) {
  if (e.key !== "Escape") return;
  enabled.value = false;
}

onBeforeUnmount(() => {
  removeListeners();
});

const listenersAttached = ref(false);
function addListeners() {
  if (listenersAttached.value) return;
  window.addEventListener("mousemove", onMove, true);
  window.addEventListener("click", onClick, true);
  window.addEventListener("keydown", onKeyDown, true);
  listenersAttached.value = true;
}
function removeListeners() {
  if (!listenersAttached.value) return;
  window.removeEventListener("mousemove", onMove, true);
  window.removeEventListener("click", onClick, true);
  window.removeEventListener("keydown", onKeyDown, true);
  listenersAttached.value = false;
}

onMounted(() => {
  if (enabled.value) addListeners();
});

watch(enabled, (isEnabled) => {
  if (isEnabled) addListeners();
  else removeListeners();
});
</script>

<style>
.overlay-ui-root {
  pointer-events: auto;
}
.selection-overlay-content {
  position: fixed;
  inset: 0;
  display: block;
  pointer-events: none;
}
.description-alert {
  left: 16px;
  right: 16px;
  bottom: 16px;
}
.rect-overlay.v-sheet {
  background: rgba(255, 64, 129, 0.08) !important;
  border: 2px solid orange !important;
  box-sizing: border-box;
}
</style>
