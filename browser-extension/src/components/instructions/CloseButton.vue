<template>
  <v-btn
    @click="() => emit('close')"
    size="large"
    block
    color="warning"
    :prepend-icon="mdiClose"
  >
    {{ i18n.t("instructions.closeButton.text") }}
    <v-tooltip
      activator="parent"
      location="bottom"
    >
      {{ i18n.t("instructions.closeButton.tooltip") }}
    </v-tooltip>
  </v-btn>
</template>

<script setup lang="ts">
import { mdiClose } from "@mdi/js";
import { i18n } from "#i18n";
import { VBtn, VTooltip } from "vuetify/components";

const emit = defineEmits<{
  close: [];
}>();
</script>
