<template>
  <v-app style="width: 800px">
    <v-container>
      <p>Das ist ein Test</p>
      <v-btn :prepend-icon="mdiAccessPoint">Das ist ein Test</v-btn>
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { mdiAccessPoint } from "@mdi/js";
import { VApp, VBtn, VContainer } from "vuetify/components";
</script>
