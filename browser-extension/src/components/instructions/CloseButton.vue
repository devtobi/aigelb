<template>
  <v-btn
    @click="() => emit('close')"
    size="large"
    block
    color="warning"
    :prepend-icon="mdiClose"
  >
    Anleitung schließen
    <v-tooltip
      activator="parent"
      location="bottom"
      >Die Anleitung kann jederzeit wieder über das AIGELB-Symbol in der
      Browserleiste geöffnet werden.</v-tooltip
    >
  </v-btn>
</template>

<script setup lang="ts">
import { mdiClose } from "@mdi/js";
import { VBtn, VTooltip } from "vuetify/components";

const emit = defineEmits<{
  close: [];
}>();
</script>
