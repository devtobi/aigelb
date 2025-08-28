<template>
  <v-dialog
    :model-value="show"
    persistent
    max-width="400"
  >
    <v-card
      :title="i18n.t('instructions.closeDialog.title')"
      class="pa-3"
    >
      <v-card-text class="text-body-2">
        {{ i18n.t("instructions.closeDialog.description") }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          :text="i18n.t('common.cancel')"
          @click="emit('cancel')"
        />
        <v-btn
          :text="i18n.t('common.close')"
          @click="emit('close')"
          color="warning"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { i18n } from "#i18n";

defineProps<{
  show: boolean;
}>();

const emit = defineEmits<{
  close: [];
  cancel: [];
}>();
</script>
