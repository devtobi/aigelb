<template>
  <v-expansion-panels>
    <v-expansion-panel elevation="3">
      <template #title>
        <h2 class="text-h6">Weiterführende Links</h2>
      </template>
      <template #text>
        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <card-link
              title="AIGELB auf GitHub"
              subtitle="Verfolge die Entwicklung von AIGELB"
              link="https://github.com/devtobi/aigelb/"
              :icon="mdiGithub"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <card-link
              title="Wissenschaftliche Arbeit zu AIGELB"
              subtitle="Erscheint in 2026"
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
import {
  VCol,
  VExpansionPanel,
  VExpansionPanels,
  VRow,
} from "vuetify/components";

import CardLink from "@/components/common/CardLink.vue";
</script>
