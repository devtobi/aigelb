<template>
  <v-expansion-panel elevation="3">
    <template #title>
      <v-icon
        :icon="mdiCog"
        class="mr-2"
      />
      <h2 class="text-h6">
        {{ cardTitle }}
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
                :title="ollamaStepTitle"
                value="1"
                :complete="isOllamaAvailable"
                elevation="0"
                :error="ollamaStepInteracted"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.setupCard.ollamaStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="warning"
                >
                  {{ i18n.t("instructions.setupCard.ollamaStep.alert") }}
                </v-alert>

                <template #next>
                  <v-btn
                    :color="ollamaStepInteracted ? 'error' : 'warning'"
                    @click="
                      interact(step, runOllamaCheck(jumpToNextUncompletedStep))
                    "
                  >
                    {{
                      ollamaStepInteracted
                        ? i18n.t("common.retry")
                        : i18n.t("instructions.setupCard.ollamaStep.nextText")
                    }}
                  </v-btn>
                </template>
                <template v-slot:prev>
                  <v-btn
                    :prepend-icon="mdiDownload"
                    variant="tonal"
                    :text="
                      i18n.t('instructions.setupCard.ollamaStep.downloadText')
                    "
                    href="https://ollama.com/download"
                    target="_blank"
                    :disabled="false"
                  />
                </template>
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="modelStepTitle"
                value="2"
                elevation="0"
                :complete="isModelAvailable"
                :error="modelStepInteracted"
              >
                <p class="mb-3">
                  {{
                    i18n
                      .t("instructions.setupCard.modelStep.description")
                      .replace("%s", LLM_HUGGINGFACE_REPO)
                  }}
                </p>

                <v-alert
                  color="warning"
                  type="warning"
                >
                  {{ i18n.t("instructions.setupCard.modelStep.alert") }}
                </v-alert>
                <template #next>
                  <v-btn
                    v-if="isModelAvailable"
                    :color="modelStepInteracted ? 'error' : 'warning'"
                    @click="
                      interact(step, runModelCheck(jumpToNextUncompletedStep))
                    "
                  >
                    {{
                      modelStepInteracted
                        ? i18n.t("common.retry")
                        : i18n.t("common.next")
                    }}
                  </v-btn>
                </template>
                <template v-slot:prev>
                  <model-download-button
                    v-if="!isModelAvailable"
                    color="warning"
                    :repo="LLM_HUGGINGFACE_REPO"
                    :file="LLM_HUGGINGFACE_FILE"
                    @download-completed="runModelCheck"
                  />
                </template>
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="pinStepTitle"
                value="3"
                :complete="!!isPinned"
                elevation="0"
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.setupCard.pinStep.description") }}
                </p>

                <v-alert
                  color="warning"
                  type="info"
                >
                  {{ i18n.t("instructions.setupCard.pinStep.alert") }}
                </v-alert>

                <template #next="{ next }">
                  <v-btn
                    color="warning"
                    @click="interact(step, next)"
                  >
                    {{
                      isPinned ? i18n.t("common.next") : i18n.t("common.skip")
                    }}
                  </v-btn>
                </template>
                <template v-slot:prev />
              </v-stepper-vertical-item>
              <v-stepper-vertical-item
                :title="i18n.t('instructions.setupCard.doneStep.title')"
                value="4"
                :complete="
                  !!isOllamaAvailable && !!isModelAvailable && currentStep === 4
                "
                elevation="0"
                hide-actions
              >
                <p class="mb-3">
                  {{ i18n.t("instructions.setupCard.doneStep.description") }}
                </p>
              </v-stepper-vertical-item>
            </template>
          </v-stepper-vertical>
        </v-card-text>
      </v-card>
    </template>
  </v-expansion-panel>
</template>

<script setup lang="ts">
import { mdiCog, mdiDownload } from "@mdi/js";
import { i18n } from "#i18n";
import {
  computed,
  onMounted,
  onUnmounted,
  ref,
  useTemplateRef,
  watch,
} from "vue";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";
import { browser } from "wxt/browser";

import ModelDownloadButton from "@/components/instructions/ModelDownloadButton.vue";
import { useBrowser } from "@/composables/useBrowser.ts";
import { useModelAvailability } from "@/composables/useModelAvailability.ts";
import { useOllama } from "@/composables/useOllama.ts";
import { useStepperInteractions } from "@/composables/useStepperInteractions.ts";
import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config.ts";

const emit = defineEmits<{
  onboardingCompletedChanged: [value: boolean];
}>();

// Stepper setup
onMounted(async () => {
  browser.action.onUserSettingsChanged?.addListener(updatePinStatus);
  await jumpToNextUncompletedStep();
});
async function checkStatus() {
  await updatePinStatus();
  await checkOllamaConnection();
  await checkModelAvailable();
}
async function jumpToNextUncompletedStep() {
  await checkStatus();
  if (!isOllamaAvailable.value) {
    currentStep.value = 1;
  } else if (!isModelAvailable.value) {
    currentStep.value = 2;
  } else if (!isPinned.value) {
    currentStep.value = 3;
  } else {
    currentStep.value = 4;
  }
}

// Tracking manual interactions
const stepper = useTemplateRef("stepper");
const { manualInteractions, interact } = useStepperInteractions(stepper);
const ollamaStepInteracted = computed(
  () => isOllamaAvailable.value === false && manualInteractions.value[0]
);
const modelStepInteracted = computed(
  () => isModelAvailable.value === false && manualInteractions.value[1]
);
const currentStep = ref(1);

// Ollama check
const { isOllamaAvailable, checkOllamaConnection } = useOllama();
async function runOllamaCheck(next?: () => void) {
  const ok = await checkOllamaConnection();
  if (ok && next) next();
}
const ollamaStepTitle = computed(() => {
  let suffix = " ";
  if (isOllamaAvailable.value === true) {
    suffix = ` (${i18n.t("instructions.setupCard.ollamaStep.successSuffix")})`;
  } else if (ollamaStepInteracted.value === true) {
    suffix = ` (${i18n.t("instructions.setupCard.ollamaStep.failureSuffix")})`;
  }
  return `${i18n.t("instructions.setupCard.ollamaStep.title")}${suffix}`;
});

// Model check
const { isModelAvailable, checkModelAvailable } = useModelAvailability();
async function runModelCheck(next?: () => void) {
  const ok = await checkModelAvailable();
  if (ok && next) next();
}
const modelStepTitle = computed(() => {
  let suffix = " ";
  if (isModelAvailable.value === true) {
    suffix = ` (${i18n.t("instructions.setupCard.modelStep.successSuffix")})`;
  } else if (modelStepInteracted.value === true) {
    suffix = ` (${i18n.t("instructions.setupCard.modelStep.failureSuffix")})`;
  }
  return `${i18n.t("instructions.setupCard.modelStep.title")}${suffix}`;
});

const setupCompleted = computed(
  () => !!isOllamaAvailable.value && !!isModelAvailable.value
);
watch(
  setupCompleted,
  (newSetupCompleted) => {
    emit("onboardingCompletedChanged", newSetupCompleted);
  },
  { immediate: true }
);
const cardTitle = computed(() => {
  let suffix;
  if (setupCompleted.value) {
    suffix = ` (${i18n.t("instructions.setupCard.successSuffix")})`;
  } else {
    suffix = ` (${i18n.t("instructions.setupCard.failureSuffix")})`;
  }
  return `${i18n.t("instructions.setupCard.title")}${suffix}`;
});

// Pin check
const { isPinnedInToolbar } = useBrowser();
const isPinned = ref<boolean | null>(false);
async function updatePinStatus() {
  isPinned.value = await isPinnedInToolbar();
}
onUnmounted(() => {
  browser.action.onUserSettingsChanged?.removeListener(updatePinStatus);
});
watch(isPinned, (newIsPinned) => {
  if (currentStep.value > 3 && !newIsPinned) {
    currentStep.value = 3;
  }
});
const pinStepTitle = computed(() => {
  let suffix;
  if (isPinned.value) {
    suffix = ` (${i18n.t("instructions.setupCard.pinStep.successSuffix")})`;
  } else {
    suffix = ` (${i18n.t("common.optional")})`;
  }
  return `${i18n.t("instructions.setupCard.pinStep.title")}${suffix}`;
});
</script>
