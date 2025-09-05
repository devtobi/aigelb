<template>
  <v-btn
    :loading="downloading"
    :prepend-icon="mdiDownload"
    variant="tonal"
    :text="downloadText"
    :disabled="disabled"
    @click="downloadModel"
  >
    <template #loader>
      <div>
        <v-progress-circular
          :model-value="downloadProgressPercent"
          size="20"
          class="mr-2"
          color="warning"
        />
        <span>{{ downloadProgress }}</span>
      </div>
    </template>
  </v-btn>
</template>
<script setup lang="ts">
import type { ModelData } from "@/types/ModelData.ts";
import type { RemoveListenerCallback } from "@webext-core/messaging";

import { mdiDownload } from "@mdi/js";
import { i18n } from "#i18n";
import { computed, onMounted, ref, watch } from "vue";

import { convertFileSize, convertToOllamaUrl } from "@/utility/conversion.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

const props = withDefaults(
  defineProps<{
    disabled?: boolean;
    repo: string;
    file: string;
  }>(),
  {
    disabled: false,
  }
);

const fileSize = ref<number | null>(0);
const downloading = ref<boolean>(false);
const downloadProgressPercent = ref<number>(0);
const downloadProgress = computed(
  () => `${downloadProgressPercent.value.toFixed(1)}%`
);
const removeListenerCallBack = ref<RemoveListenerCallback>();

onMounted(async () => {
  const modelData: ModelData = {
    repo: props.repo,
    file: props.file,
  };
  fileSize.value = await sendMessage("getModelSize", modelData);
});

const downloadText = computed(() => {
  const fileSizeReadable = fileSize.value
    ? ` (${convertFileSize(fileSize.value)})`
    : "";
  return `${i18n.t("instructions.modelDownloadButton.text")}${fileSizeReadable}`;
});

const emit = defineEmits<{
  downloadCompleted: [];
}>();
const ollamaPullUrl = computed(() =>
  convertToOllamaUrl(props.repo, props.file)
);
async function downloadModel() {
  downloadProgressPercent.value = 0;
  downloading.value = true;
  await sendMessage("downloadModel", ollamaPullUrl.value);
}
watch(
  () => downloading.value,
  (newDownloading) => {
    if (newDownloading) {
      if (removeListenerCallBack.value) {
        resetListeners();
      }
      removeListenerCallBack.value = onMessage(
        "downloadProgress",
        (progress) => {
          downloadProgressPercent.value = progress.data.percentage;
          if (progress.data.status === "completed") {
            emit("downloadCompleted");
            downloading.value = false;
          }
        }
      );
    } else {
      resetListeners();
    }
  }
);
function resetListeners() {
  removeListenerCallBack.value?.();
  removeListenerCallBack.value = undefined;
}
</script>
