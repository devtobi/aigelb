<template>
  <v-expansion-panel elevation="3">
    <template #title>
      <v-icon
        :icon="mdiTooltipQuestion"
        class="mr-2"
      />
      <h2 class="text-h6">
        {{ i18n.t("instructions.usageCard.title") }}
      </h2>
    </template>
    <template #text>
      <v-card class="elevation-0">
        <v-card-text class="pa-0">
          <v-stepper-vertical ref="stepper">
            <template #default>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.usageCard.openStep.title')"
                value="1"
                elevation="0"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.usageCard.openStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                  class="mb-3"
                >
                  {{ i18n.t("instructions.usageCard.openStep.alert") }}
                </v-alert>

                <p>{{ i18n.t("common.example") }}:</p>
                <v-img src="@/assets/de/AIGELB_openStep.png" />
                <template #prev />
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.usageCard.startSelectStep.title')"
                value="2"
                elevation="0"
              >
                <p class="mb-3">
                  {{
                    i18n.t("instructions.usageCard.startSelectStep.description")
                  }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.usageCard.startSelectStep.alert") }}
                </v-alert>
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.usageCard.selectStep.title')"
                value="3"
                elevation="0"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.usageCard.selectStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.usageCard.selectStep.alert") }}
                </v-alert>
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.usageCard.waitStep.title')"
                value="4"
                elevation="0"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.usageCard.waitStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.usageCard.waitStep.alert") }}
                </v-alert>
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.usageCard.resetStep.title')"
                value="5"
                elevation="0"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.usageCard.resetStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.usageCard.resetStep.alert") }}
                </v-alert>
                <template #next />
              </v-stepper-vertical-item>
            </template>
          </v-stepper-vertical>
        </v-card-text>
      </v-card>
    </template>
  </v-expansion-panel>
</template>

<script setup lang="ts">
import { mdiTooltipQuestion } from "@mdi/js";
import { i18n } from "#i18n";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";
import { getUILanguage } from "@/utility/browser.ts";

const uiLanguage = getUILanguage();

function getImageUrl(filePath: string) {
  return `${filePath}_${uiLanguage}.png`;
}
</script>
