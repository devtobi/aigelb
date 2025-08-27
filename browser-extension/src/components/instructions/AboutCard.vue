<template>
  <v-card
    title="Über AIGELB"
    :prepend-icon="mdiInformation"
    class="pa-3"
    elevation="3"
  >
    <v-card-text>
      <p>
        AIGELB is a browser extension designed to improve accessibility by
        simplifying German texts into <strong>Easy Language</strong>. This makes
        web content more understandable for people with different reading
        abilities.
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { mdiInformation } from "@mdi/js";
import { VCard, VCardText } from "vuetify/components";
</script>
