<template>
  <v-card
    :title="i18n.t('instructions.aboutCard.title')"
    :prepend-icon="mdiInformation"
    class="pa-3"
    elevation="3"
  >
    <v-card-text>
      <p class="mb-3">
        {{ i18n.t("instructions.aboutCard.description") }}
      </p>
      <p class="mb-3">
        {{ i18n.t("instructions.aboutCard.problem") }}
      </p>
      <p>
        {{ i18n.t("instructions.aboutCard.background") }}
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { mdiInformation } from "@mdi/js";
import { i18n } from "#i18n";
</script>
