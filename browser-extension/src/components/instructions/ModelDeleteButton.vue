<template>
  <v-btn
    :prepend-icon="mdiTrashCan"
    variant="tonal"
    color="error"
    :text="i18n.t('instructions.modelDeleteButton.text')"
    :disabled="disabled"
    @click="deleteModel"
  />
</template>
<script setup lang="ts">
import { mdiTrashCan } from "@mdi/js";
import { i18n } from "#i18n";
import { computed } from "vue";

import { convertToOllamaUrl } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

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

const emit = defineEmits<{
  deleteCompleted: [];
}>();
const ollamaPullUrl = computed(() =>
  convertToOllamaUrl(props.repo, props.file)
);
async function deleteModel() {
  await sendMessage("deleteModel", ollamaPullUrl.value);
  emit("deleteCompleted");
}
</script>
