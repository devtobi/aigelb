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
      {{ rect.x }}, {{ rect.y }}, {{ rect.w }}, {{ rect.h }}, {{ rect.visible }}
      <v-sheet
        v-show="rect.visible"
        :elevation="4"
        rounded="lg"
        class="pointer-events-none position-fixed"
        :style="{
          left: rect.x + 'px',
          top: rect.y + 'px',
          width: rect.w + 'px',
          height: rect.h + 'px',
          zIndex: 2147483647,
          border: '2px solid #ff4081',
          background: 'rgba(255, 64, 129, 0.08)',
          boxShadow: '0 0 0 1px rgba(0,0,0,.08) inset',
        }"
      />

      <!-- 4) Bottom instruction alert while selection mode is active -->
      <v-alert
        v-if="enabled"
        color="orange"
        type="info"
        variant="elevated"
        rounded="lg"
        class="pa-3 position-fixed"
        :style="{
          left: '16px',
          right: '16px',
          bottom: '16px',
          zIndex: 2147483647,
        }"
        prominent
        border="start"
        title="Selection mode"
        text="Hover to highlight any element. Click to log it. Press Esc to exit."
      >
        <template #append>
          <v-btn
            variant="text"
            @click="enabled = false"
            >Cancel</v-btn
          >
        </template>
      </v-alert>
    </div>
  </v-overlay>
</template>

<script setup lang="ts">
import {
  defineModel,
  onBeforeUnmount,
  onMounted,
  reactive,
  useTemplateRef,
} from "vue";

const enabled = defineModel<boolean>();

// Reactive state for the hover rectangle and label
const rect = reactive({ x: 0, y: 0, w: 0, h: 0, visible: false });

// Ref to the overlay UI root (teleported content wrapper)
const overlayUi = useTemplateRef<HTMLElement>("overlayUi");

// Robust hit-testing: use elementsFromPoint and filter out our overlay + shadow host.
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
    // Skip any element inside our overlay UI (defensive; should be excluded via pointer-events)
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
  // If the click originated inside our overlay UI, do not intercept it.
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
}

onMounted(() => {
  window.addEventListener("mousemove", onMove, true);
  window.addEventListener("click", onClick, true);
});
onBeforeUnmount(() => {
  window.removeEventListener("mousemove", onMove, true);
  window.removeEventListener("click", onClick, true);
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
/* Ensure VOverlay's content wrapper fills the viewport inside the shadow root */
.selection-overlay-content {
  position: fixed;
  inset: 0;
  display: block;
  pointer-events: none;
}
.pointer-events-none {
  pointer-events: none;
}
</style>
