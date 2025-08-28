<template>
  <v-expansion-panel elevation="3">
    <template #title>
      <v-icon
        :icon="mdiInformation"
        class="mr-2"
      />
      <h2 class="text-h6">{{ i18n.t("instructions.linksPanel.title") }}</h2>
    </template>
    <template #text>
      <v-row>
        <v-col
          cols="12"
          md="6"
        >
          <card-link
            :title="i18n.t('instructions.linksPanel.github.title')"
            :subtitle="i18n.t('instructions.linksPanel.github.subTitle')"
            link="https://github.com/devtobi/aigelb/"
            :icon="mdiGithub"
          />
        </v-col>
        <v-col
          cols="12"
          md="6"
        >
          <card-link
            :title="i18n.t('instructions.linksPanel.paper.title')"
            :subtitle="i18n.t('instructions.linksPanel.paper.subTitle')"
            :icon="mdiSchool"
          />
        </v-col>
      </v-row>
    </template>
  </v-expansion-panel>
</template>

<script setup lang="ts">
import { mdiGithub, mdiInformation, mdiSchool } from "@mdi/js";
import { i18n } from "#i18n";

import CardLink from "@/components/common/CardLink.vue";
</script>
