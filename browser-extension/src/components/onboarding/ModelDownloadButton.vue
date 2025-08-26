<template>
  <v-btn
    :prepend-icon="mdiDownload"
    variant="tonal"
    :text="downloadText"
    :disabled="disabled"
  >
    <template #loader>
      <v-progress-circular
        class="mt-3"
        :model-value="downloadProgressPercent"
        color="warning"
        indeterminate
      />
    </template>
  </v-btn>
</template>
<script setup lang="ts">
import { mdiDownload } from "@mdi/js";
import { computed, onMounted, ref } from "vue";
import { VBtn, VProgressCircular } from "vuetify/components";

import { convertFileSize } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

const props = defineProps<{
  disabled: boolean;
  repo: string;
  file: string;
}>();

const fileSize = ref<number | null>(0);
const downloadProgressPercent = ref<number>(0);

onMounted(async () => {
  fileSize.value = await sendMessage("getModelSize", {
    repo: props.repo,
    file: props.file,
  });
});

const downloadText = computed(() => {
  const fileSizeReadable = fileSize.value
    ? ` (${convertFileSize(fileSize.value)})`
    : "";
  return `Modell herunterladen${fileSizeReadable}`;
});
</script>
