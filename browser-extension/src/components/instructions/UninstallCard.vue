<template>
  <v-expansion-panels>
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
                      @delete-completed="checkModelAvailable"
                    />
                    <v-btn
                      v-else
                      :color="modelStepInteracted ? 'error' : 'warning'"
                      @click="
                        interact(
                          step,
                          checkModelAvailable(jumpToNextUncompletedStep)
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
                      i18n.t(
                        "instructions.uninstallCard.ollamaStep.description"
                      )
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
                          checkOllamaNotAvailable(jumpToNextUncompletedStep)
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
                    {{
                      i18n.t("instructions.uninstallCard.extensionStep.alert")
                    }}
                  </v-alert>
                </v-stepper-vertical-item>
              </template>
            </v-stepper-vertical>
          </v-card-text>
        </v-card>
      </template>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { mdiTrashCanOutline } from "@mdi/js";
import { i18n } from "#i18n";
import { computed, onMounted, ref, useTemplateRef, watch } from "vue";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";

import ModelDeleteButton from "@/components/instructions/ModelDeleteButton.vue";
import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config.ts";
import { convertToOllamaUrl } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

onMounted(async () => {
  await jumpToNextUncompletedStep();
});
async function checkStatus() {
  await checkModelAvailable();
  await checkOllamaNotAvailable();
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
const stepCount = computed(() => {
  const stepperEl = stepper.value?.$el as HTMLElement | undefined;
  if (!stepperEl) return 0;
  return stepperEl.querySelectorAll(".v-stepper-vertical-item").length;
});
const manualInteractions = ref<boolean[]>([]);
const modelStepInteracted = computed(
  () => isModelAvailable.value === true && manualInteractions.value[0]
);
const ollamaStepInteracted = computed(
  () => isOllamaAvailable.value === true && manualInteractions.value[1]
);
watch(
  stepCount,
  (newStepCount) => {
    manualInteractions.value = Array(
      newStepCount > 0 ? newStepCount - 1 : 0
    ).fill(false);
  },
  { once: true }
);
async function interact(
  step: number,
  interactionFunction: Promise<void> | (() => void)
) {
  manualInteractions.value[step - 1] = true;
  if (interactionFunction instanceof Promise) {
    await interactionFunction;
  } else {
    interactionFunction();
  }
}
const currentStep = ref(1);

// Model deletion check
const isModelAvailable = ref<boolean | undefined>(undefined);
const ollamaPullUrl = computed(() =>
  convertToOllamaUrl(LLM_HUGGINGFACE_REPO, LLM_HUGGINGFACE_FILE)
);
async function checkModelAvailable(next?: () => void) {
  isModelAvailable.value = await sendMessage(
    "checkIsModelAvailable",
    ollamaPullUrl.value
  );
  if (isModelAvailable.value === false && next) {
    next();
  }
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
const isOllamaAvailable = ref<boolean | undefined>(undefined);
async function checkOllamaNotAvailable(next?: () => void) {
  isOllamaAvailable.value = await sendMessage("checkOllamaConnection");
  if (isOllamaAvailable.value === false && next) {
    next();
  }
}
const ollamaStepTitle = computed(() => {
  let suffix = " ";
  if (isModelAvailable.value === false) {
    suffix = ` (${i18n.t("instructions.uninstallCard.ollamaStep.successSuffix")})`;
  } else if (modelStepInteracted.value === true) {
    suffix = ` (${i18n.t("instructions.uninstallCard.ollamaStep.failureSuffix")})`;
  }
  return `${i18n.t("instructions.uninstallCard.ollamaStep.title")}${suffix}`;
});
</script>
