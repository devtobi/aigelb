<template>
  <v-overlay
    :model-value="enabled"
    persistent
    :scrim="false"
    :absolute="false"
    contained
    :z-index="2147483647"
    content-class="selection-overlay-content"
  >
    <div
      ref="overlayUi"
      class="overlay-ui-root"
    >
      <div
        class="selection-overlay pointer-events-none"
        aria-hidden="true"
      />
      <v-sheet
        v-show="rect.visible"
        class="pointer-events-none position-fixed rect-overlay"
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

const enabled = defineModel<boolean>();

const rect = reactive({ x: 0, y: 0, w: 0, h: 0, visible: false });

const overlayUi = useTemplateRef<HTMLElement>("overlayUi");

function getShadowHost(): HTMLElement | null {
  const ui = overlayUi.value;
  if (!ui) return null;
  const root = ui.getRootNode();
  return root instanceof ShadowRoot ? (root.host as HTMLElement) : null;
}

function elementAtClientPoint(x: number, y: number): Element | null {
  const host = getShadowHost();
  const list = document.elementsFromPoint(x, y);
  for (const el of list) {
    if (!(el instanceof Element)) continue;
    if (host && el === host) continue;
    if (el === document.documentElement || el === document.body) continue;
    const ui = overlayUi.value;
    if (ui && el instanceof Node && ui.contains(el)) continue;
    return el;
  }
  return null;
}

function onMove(e: MouseEvent) {
  if (!enabled.value) return;
  const t = elementAtClientPoint(e.clientX, e.clientY);
  if (!t || t === document.documentElement || t === document.body) {
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
  if (!enabled.value) return;
  const uiRoot = overlayUi.value;

  /* eslint-disable @typescript-eslint/no-explicit-any */
  const insideOverlay = uiRoot
    ? (typeof (e as any).composedPath === "function" &&
        (e as any).composedPath().includes(uiRoot)) ||
      (e.target instanceof Node && uiRoot.contains(e.target))
    : false;
  /* eslint-enable @typescript-eslint/no-explicit-any */
  if (insideOverlay) {
    return;
  }

  e.preventDefault();
  e.stopPropagation();
  const t = elementAtClientPoint(e.clientX, e.clientY);
  if (!t) return;
  console.debug("outerHTML:", (t as HTMLElement).outerHTML);
  // TODO
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
.selection-overlay {
  position: fixed;
  inset: 0;
  cursor: crosshair;
  background: transparent;
}
.selection-overlay-content {
  position: fixed;
  inset: 0;
  display: block;
  pointer-events: none;
}
.pointer-events-none {
  pointer-events: none;
}
.description-alert {
  left: 16px;
  right: 16px;
  bottom: 16px;
  z-index: 2147483647;
}
.rect-overlay {
  background: rgba(255, 64, 129, 0.08);
  border: 2px solid orange;
  z-index: 2147483647;
}
</style>
