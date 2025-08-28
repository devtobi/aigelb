<template>
  <v-card
    class="text-center pa-3"
    elevation="3"
  >
    <the-app-icon
      class="mx-auto"
      :size="128"
    />
    <v-card-title class="pt-0 text-h4 font-weight-bold">AIGELB</v-card-title>
    <v-card-text class="pb-4">
      <p>
        {{ i18n.t("instructions.headerCard.subTitle") }}
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { i18n } from "#i18n";

import TheAppIcon from "@/components/common/TheAppIcon.vue";
</script>
