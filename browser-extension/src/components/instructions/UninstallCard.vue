<template>
  <v-expansion-panel elevation="3">
    <template #title>
      <v-icon
        :icon="mdiTrashCanOutline"
        class="mr-2"
      />
      <h2 class="text-h6">
        {{ i18n.t("instructions.uninstallCard.title") }}
      </h2>
    </template>
    <template #text>
      <v-card class="elevation-0">
        <v-card-text class="pa-0">
          <v-stepper-vertical
            v-model="currentStep"
            ref="stepper"
          >
            <template #default="{ step }">
              <v-stepper-vertical-item
                :title="modelStepTitle"
                value="1"
                :complete="isModelAvailable === false"
                elevation="0"
                :error="modelStepInteracted"
              >
                <p class="mb-3">
                  {{
                    i18n.t("instructions.uninstallCard.modelStep.description")
                  }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.uninstallCard.modelStep.alert") }}
                </v-alert>

                <template #next>
                  <model-delete-button
                    v-if="isModelAvailable === true"
                    :repo="LLM_HUGGINGFACE_REPO"
                    :file="LLM_HUGGINGFACE_FILE"
                    @delete-completed="runModelCheckForUninstall"
                  />
                  <v-btn
                    v-else
                    :color="modelStepInteracted ? 'error' : 'warning'"
                    @click="
                      interact(
                        step,
                        runModelCheckForUninstall(jumpToNextUncompletedStep)
                      )
                    "
                  >
                    {{ i18n.t("common.next") }}
                  </v-btn>
                </template>
                <template #prev />
              </v-stepper-vertical-item>

              <v-stepper-vertical-item
                :title="ollamaStepTitle"
                value="2"
                :complete="isOllamaAvailable === false"
                :error="ollamaStepInteracted && isOllamaAvailable === true"
                elevation="0"
              >
                <p class="mb-3">
                  {{
                    i18n.t("instructions.uninstallCard.ollamaStep.description")
                  }}
                </p>

                <v-alert
                  color="warning"
                  type="warning"
                >
                  {{ i18n.t("instructions.uninstallCard.ollamaStep.alert") }}
                </v-alert>

                <template #next>
                  <v-btn
                    :color="
                      ollamaStepInteracted && isOllamaAvailable
                        ? 'error'
                        : 'warning'
                    "
                    @click="
                      interact(
                        step,
                        runOllamaNotAvailable(jumpToNextUncompletedStep)
                      )
                    "
                  >
                    {{
                      ollamaStepInteracted
                        ? i18n.t("common.retry")
                        : i18n.t(
                            "instructions.uninstallCard.ollamaStep.uninstallText"
                          )
                    }}
                  </v-btn>
                </template>
                <template #prev />
              </v-stepper-vertical-item>

              <v-stepper-vertical-item
                :title="
                  i18n.t('instructions.uninstallCard.extensionStep.title')
                "
                value="3"
                :complete="
                  currentStep === 3 &&
                  isOllamaAvailable === false &&
                  isModelAvailable === false
                "
                elevation="0"
                hide-actions
              >
                <p class="mb-3">
                  {{
                    i18n.t(
                      "instructions.uninstallCard.extensionStep.description"
                    )
                  }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.uninstallCard.extensionStep.alert") }}
                </v-alert>
              </v-stepper-vertical-item>
            </template>
          </v-stepper-vertical>
        </v-card-text>
      </v-card>
    </template>
  </v-expansion-panel>
</template>

<script setup lang="ts">
import { mdiTrashCanOutline } from "@mdi/js";
import { i18n } from "#i18n";
import { computed, onMounted, ref, useTemplateRef } from "vue";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";

import ModelDeleteButton from "@/components/instructions/ModelDeleteButton.vue";
import { useModelAvailability } from "@/composables/useModelAvailability.ts";
import { useOllama } from "@/composables/useOllama.ts";
import { useStepperInteractions } from "@/composables/useStepperInteractions.ts";
import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config.ts";

onMounted(async () => {
  await jumpToNextUncompletedStep();
});
async function checkStatus() {
  await checkModelAvailable();
  await checkOllamaConnection();
}
async function jumpToNextUncompletedStep() {
  await checkStatus();
  if (isModelAvailable.value === true) {
    currentStep.value = 1;
  } else if (isOllamaAvailable.value === true) {
    currentStep.value = 2;
  } else {
    currentStep.value = 3;
  }
}

// Stepper state
const stepper = useTemplateRef("stepper");
const { manualInteractions, interact } = useStepperInteractions(stepper);
const modelStepInteracted = computed(
  () => isModelAvailable.value === true && manualInteractions.value[0]
);
const ollamaStepInteracted = computed(
  () => isOllamaAvailable.value === true && manualInteractions.value[1]
);
const currentStep = ref(1);

// Model deletion check
const { isModelAvailable, checkModelAvailable } = useModelAvailability();
async function runModelCheckForUninstall(next?: () => void) {
  const ok = await checkModelAvailable();
  if (!ok && next) next();
}
const modelStepTitle = computed(() => {
  let suffix = " ";
  if (isModelAvailable.value === false) {
    suffix = ` (${i18n.t("instructions.uninstallCard.modelStep.successSuffix")})`;
  } else if (modelStepInteracted.value === true) {
    suffix = ` (${i18n.t("instructions.uninstallCard.modelStep.failureSuffix")})`;
  }
  return `${i18n.t("instructions.uninstallCard.modelStep.title")}${suffix}`;
});

// Ollama uninstall check
const { isOllamaAvailable, checkOllamaConnection } = useOllama();
async function runOllamaNotAvailable(next?: () => void) {
  const ok = await checkOllamaConnection();
  if (!ok && next) next();
}
const ollamaStepTitle = computed(() => {
  let suffix = " ";
  if (isOllamaAvailable.value === false) {
    suffix = ` (${i18n.t("instructions.uninstallCard.ollamaStep.successSuffix")})`;
  } else if (ollamaStepInteracted.value === true) {
    suffix = ` (${i18n.t("instructions.uninstallCard.ollamaStep.failureSuffix")})`;
  }
  return `${i18n.t("instructions.uninstallCard.ollamaStep.title")}${suffix}`;
});
</script>
