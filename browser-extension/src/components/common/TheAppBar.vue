<template>
  <v-app-bar
    :elevation="2"
    color="warning"
  >
    <v-app-bar-title class="d-flex align-center">
      <div class="d-flex align-center">
        <the-app-icon
          class="mr-5"
          :size="48"
        />
        <span>{{ title }}</span>
      </div>
    </v-app-bar-title>

    <template v-slot:append>
      <p class="text-subtitle-1 font-weight-bold mr-5">
        {{ i18n.t("common.appBar.versionPrefix") }}: {{ extensionVersion }}
      </p>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { useTitle } from "@vueuse/core";
import { i18n } from "#i18n";
import { VAppBar, VAppBarTitle } from "vuetify/components";

import TheAppIcon from "@/components/common/TheAppIcon.vue";
import { useManifestData } from "@/composables/useManifestData.ts";

const { extensionVersion } = useManifestData();
const title = useTitle();
</script>
