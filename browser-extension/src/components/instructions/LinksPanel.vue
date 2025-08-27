<template>
  <v-expansion-panels>
    <v-expansion-panel elevation="3">
      <template #title>
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
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { mdiGithub, mdiSchool } from "@mdi/js";
import { i18n } from "#i18n";
import {
  VCol,
  VExpansionPanel,
  VExpansionPanels,
  VRow,
} from "vuetify/components";

import CardLink from "@/components/common/CardLink.vue";
</script>
