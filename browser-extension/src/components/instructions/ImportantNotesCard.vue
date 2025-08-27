<template>
  <v-card
    title="Wichtige Hinweise"
    :prepend-icon="mdiAlert"
    color="error"
    class="pa-3"
    elevation="3"
  >
    <v-card-text>
      <p>
        AIGELB is currently in an
        <strong>early development stage</strong>. Some translations may be
        experimental or incomplete.
      </p>
      <p>
        The project originates from accessibility research in
        <strong>German Easy Language</strong> and aims to help make the web more
        inclusive.
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { mdiAlert } from "@mdi/js";
import { VCard, VCardText } from "vuetify/components";
</script>
