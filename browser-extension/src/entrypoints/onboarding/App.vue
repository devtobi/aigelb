<template>
  <v-app>
    <the-app-bar />

    <v-main class="d-flex align-center justify-center">
      <v-container>
        <!-- Header -->
        <v-card
          class="text-center mb-8 pa-3"
          elevation="3"
        >
          <the-app-icon
            class="mx-auto"
            :size="128"
          />
          <v-card-title class="pt-0 text-h2 font-weight-bold"
            >AIGELB</v-card-title
          >
          <v-card-text class="pb-4">
            <p>
              {{ i18n.t("onboarding.header.subTitle") }}
            </p>
          </v-card-text>
        </v-card>

        <!-- About -->
        <v-card
          title="Über AIGELB"
          :prepend-icon="mdiInformation"
          class="mb-8 pa-3"
          elevation="3"
        >
          <v-card-text>
            <p>
              AIGELB is a browser extension designed to improve accessibility by
              simplifying German texts into <strong>Easy Language</strong>. This
              makes web content more understandable for people with different
              reading abilities.
            </p>
          </v-card-text>
        </v-card>

        <!-- Setup Instructions -->
        <v-card
          title="Ersteinrichtung"
          :prepend-icon="mdiCog"
          class="mb-8 pa-3"
          elevation="3"
        >
          <v-card-text>
            <setup-stepper />
          </v-card-text>
        </v-card>

        <!-- Additional Notes -->
        <v-card
          title="Wichtige Hinweise"
          :prepend-icon="mdiAlert"
          color="error"
          class="mb-8 pa-3"
          elevation="3"
        >
          <v-card-text>
            <p>
              AIGELB is currently in an
              <strong>early development stage</strong>. Some translations may be
              experimental or incomplete.
            </p>
            <p>
              The project originates from accessibility research in
              <strong>German Easy Language</strong> and aims to help make the
              web more inclusive.
            </p>
          </v-card-text>
        </v-card>

        <!-- Links -->
        <v-expansion-panels class="mb-8">
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

        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              size="large"
              block
              :prepend-icon="mdiCog"
              @click="openOptionsPage"
            >
              Optionen öffnen
              <v-tooltip
                activator="parent"
                location="bottom"
                >Die Optionen können auch über das AIGELB-Symbol in der
                Browserleiste geöffnet werden.</v-tooltip
              >
            </v-btn>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              @click="closeWindow"
              size="large"
              block
              color="warning"
              :prepend-icon="mdiClose"
            >
              Informationsseite schließen
              <v-tooltip
                activator="parent"
                location="bottom"
                >Die Informationen können jederzeit wieder über das
                AIGELB-Symbol in der Browserleiste geöffnet werden.</v-tooltip
              >
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import {
  mdiAlert,
  mdiClose,
  mdiCog,
  mdiGithub,
  mdiInformation,
  mdiSchool,
} from "@mdi/js";
import { i18n } from "#i18n";
import {
  VApp,
  VBtn,
  VCard,
  VCardText,
  VCardTitle,
  VCol,
  VContainer,
  VExpansionPanel,
  VExpansionPanels,
  VMain,
  VRow,
  VTooltip,
} from "vuetify/components";

import CardLink from "@/components/common/CardLink.vue";
import TheAppBar from "@/components/common/TheAppBar.vue";
import TheAppIcon from "@/components/common/TheAppIcon.vue";
import SetupStepper from "@/components/onboarding/SetupStepper.vue";
import { useBrowser } from "@/composables/useBrowser.ts";

const { openOptionsPage, closeWindow } = useBrowser();
</script>
