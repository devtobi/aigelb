<template>
  <v-btn
    :text="i18n.t('popup.instructionsButton.text')"
    @click="openInstructions"
    size="large"
    block
    color="warning"
    :prepend-icon="mdiHelp"
  />
</template>

<script setup lang="ts">
import { mdiHelp } from "@mdi/js";
import { i18n } from "#i18n";

import { openInstructions } from "@/utility/browser.ts";
</script>
