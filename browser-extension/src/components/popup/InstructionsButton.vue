<template>
  <v-btn
    :text="i18n.t('popup.instructionsButton.text')"
    @click="openInstructions"
    size="large"
    block
    color="warning"
    :prepend-icon="mdiOpenInNew"
  />
</template>

<script setup lang="ts">
import { mdiOpenInNew } from "@mdi/js";
import { i18n } from "#i18n";

import { openInstructions } from "@/utility/browser.ts";
</script>
