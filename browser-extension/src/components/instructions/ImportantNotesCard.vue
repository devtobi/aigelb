<template>
  <v-card
    :title="i18n.t('instructions.importantNotesCard.title')"
    :prepend-icon="mdiAlert"
    color="error"
    class="pa-3"
    elevation="3"
  >
    <v-card-text>
      <p class="mb-3">
        {{ i18n.t("instructions.importantNotesCard.description") }}
      </p>
      <p>
        {{ i18n.t("instructions.importantNotesCard.development") }}
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { mdiAlert } from "@mdi/js";
import { i18n } from "#i18n";
</script>
