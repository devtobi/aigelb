<template>
  <v-overlay
    :model-value="isEnabled"
    persistent
    :scrim="false"
    :absolute="false"
    contained
    content-class="translation-overlay-content"
  >
    <div ref="overlayUi">
      <v-skeleton-loader
        v-show="rect.visible"
        class="rect-overlay pointer-events-none position-fixed border border-warning border-md"
        color="rgba(var(--v-theme-warning), 0.3)"
        :width="rect.w"
        :height="rect.h"
        :style="{
          left: rect.x + 'px',
          top: rect.y + 'px',
        }"
      />

      <v-alert
        v-if="isEnabled"
        color="warning"
        type="info"
        :icon="mdiChatProcessing"
        variant="elevated"
        class="pa-3 position-fixed description-alert"
        prominent
        :title="i18n.t('content.translationOverlay.title')"
        :text="i18n.t('content.translationOverlay.description')"
      >
        <template #append>
          <v-btn
            variant="text"
            @click="abortInference"
            size="small"
            :loading="aborting"
            :text="i18n.t('common.cancel')"
          />
        </template>
      </v-alert>
    </div>
  </v-overlay>
</template>

<script setup lang="ts">
import { mdiChatProcessing } from "@mdi/js";
import { i18n } from "#i18n";
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  reactive,
  useTemplateRef,
  watch,
} from "vue";

import { sendMessage } from "@/utility/messaging.ts";

const props = defineProps<{
  element: HTMLElement | null;
}>();

const isEnabled = computed(() => !!props.element);

const rect = reactive({ x: 0, y: 0, w: 0, h: 0, visible: false });
const overlayUi = useTemplateRef<HTMLElement>("overlayUi");
const aborting = ref<boolean>(false);

let resizeObserver: ResizeObserver | null = null;

function updateRect() {
  if (!props.element) {
    rect.visible = false;
    return;
  }
  const r = props.element.getBoundingClientRect();
  rect.x = Math.round(r.left);
  rect.y = Math.round(r.top);
  rect.w = Math.round(r.width);
  rect.h = Math.round(r.height);
  rect.visible = rect.w > 0 && rect.h > 0;
}

function attachObservers() {
  detachObservers();
  if (!props.element) return;
  resizeObserver = new ResizeObserver(() => updateRect());
  resizeObserver.observe(props.element);
  window.addEventListener("scroll", updateRect, true);
  window.addEventListener("resize", updateRect, true);
}

function detachObservers() {
  if (resizeObserver) {
    resizeObserver.disconnect();
    resizeObserver = null;
  }
  window.removeEventListener("scroll", updateRect, true);
  window.removeEventListener("resize", updateRect, true);
}

onMounted(() => {
  if (props.element) {
    attachObservers();
    updateRect();
  }
});

onBeforeUnmount(() => {
  detachObservers();
});

watch(
  () => props.element,
  (el) => {
    if (el) {
      attachObservers();
      updateRect();
    } else {
      detachObservers();
      rect.visible = false;
    }
  }
);

async function abortInference() {
  aborting.value = true;
  await sendMessage("abortInference");
}

watch(
  () => isEnabled.value,
  (enabled) => {
    if (!enabled) aborting.value = false;
  }
);
</script>

<style>
.translation-overlay-content {
  position: fixed;
  inset: 0;
  display: block;
}
.description-alert {
  left: 16px;
  right: 16px;
  bottom: 16px;
}
</style>
