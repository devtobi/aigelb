<template>
  <v-card
    title="Ersteinrichtung"
    :prepend-icon="mdiCog"
    class="pa-3"
    elevation="3"
  >
    <v-card-text>
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
              Für die lokale Ausführung der KI-Modelle ist die Software Ollama
              erforderlich.
            </p>

            <p class="mb-3">
              Diese muss von der Webseite des Herstellers heruntergeladen und
              anschließend gestartet werden.
            </p>

            <v-alert
              color="warning"
              type="info"
            >
              Ollama muss während der Nutzung von AIGELB im Hintergrund
              ausgeführt werden, damit die Browsererweiterung funktioniert. Je
              nach Betriebssystem muss Ollama z.B. nach dem Systemstart manuell
              gestartet werden.
            </v-alert>

            <template #next>
              <v-btn
                :color="ollamaStepInteracted ? 'error' : 'warning'"
                @click="
                  interact(
                    step,
                    checkOllamaConnection(jumpToNextUncompletedStep)
                  )
                "
              >
                {{
                  ollamaStepInteracted
                    ? "Erneut versuchen"
                    : "Verbindung prüfen"
                }}
              </v-btn>
            </template>
            <template v-slot:prev>
              <v-btn
                :prepend-icon="mdiDownload"
                variant="tonal"
                text="Ollama herunterladen"
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
            <p>TODO</p>
            <template #next>
              <v-btn
                v-if="isModelAvailable"
                :color="modelStepInteracted ? 'error' : 'warning'"
                @click="
                  interact(step, checkModelAvailable(jumpToNextUncompletedStep))
                "
              >
                {{ modelStepInteracted ? "Erneut versuchen" : "Weiter" }}
              </v-btn>
            </template>
            <template v-slot:prev>
              <model-download-button
                v-if="!isModelAvailable"
                color="warning"
                :repo="LLM_HUGGINGFACE_REPO"
                :file="LLM_HUGGINGFACE_FILE"
                @download-completed="checkModelAvailable"
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
              Für die einfache Nutzung der Browsererweiterung sollte diese über
              die Browserleiste fest angeheftet werden.
            </p>

            <p>
              Eine Anleitung hierzu ist auf den Hilfe-Seiten des Browsers zu
              finden.
            </p>

            <template #next="{ next }">
              <v-btn
                color="warning"
                @click="interact(step, next)"
              >
                {{ isPinned ? "Weiter" : "Überspringen" }}
              </v-btn>
            </template>
            <template v-slot:prev />
          </v-stepper-vertical-item>
          <v-stepper-vertical-item
            title="Einrichtung abgeschlossen"
            value="4"
            :complete="
              !!isOllamaAvailable && !!isModelAvailable && currentStep === 4
            "
            elevation="0"
            hide-actions
          >
            <p class="mb-3">
              Herzlichen Glückwunsch! Die Einrichtung der Browserweiterung ist
              abgeschlossen!
            </p>

            <p>
              Bitte lies dir als Nächstes die Anleitung zur Nutzung der
              Erweiterung durch.
            </p>
          </v-stepper-vertical-item>
        </template>
      </v-stepper-vertical>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { mdiCog, mdiDownload } from "@mdi/js";
import {
  computed,
  onMounted,
  onUnmounted,
  ref,
  useTemplateRef,
  watch,
} from "vue";
import { VAlert, VBtn, VCard, VCardText } from "vuetify/components";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";
import { browser } from "wxt/browser";

import ModelDownloadButton from "@/components/instructions/ModelDownloadButton.vue";
import { useBrowser } from "@/composables/useBrowser.ts";
import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config.ts";
import { convertToOllamaUrl } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

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
const stepCount = computed(() => {
  const stepperEl = stepper.value?.$el as HTMLElement | undefined;
  if (!stepperEl) return 0;
  return stepperEl.querySelectorAll(".v-stepper-vertical-item").length;
});
const manualInteractions = ref<boolean[]>([]);
const ollamaStepInteracted = computed(
  () => isOllamaAvailable.value === false && manualInteractions.value[0]
);
const modelStepInteracted = computed(
  () => isModelAvailable.value === false && manualInteractions.value[1]
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

// Ollama check
const isOllamaAvailable = ref<boolean | undefined>(undefined);
async function checkOllamaConnection(next?: () => void) {
  isOllamaAvailable.value = await sendMessage("checkOllamaConnection");
  if (isOllamaAvailable.value) {
    if (next) {
      next();
    }
  }
}
const ollamaStepTitle = computed(() => {
  let suffix = " ";
  if (isOllamaAvailable.value === true) {
    suffix = " (Verbindung erfolgreich)";
  } else if (ollamaStepInteracted.value === true) {
    suffix = " (Verbindung fehlgeschlagen)";
  }
  return `KI-Software installieren und starten${suffix}`;
});

// Model check
const isModelAvailable = ref<boolean | undefined>(undefined);
const ollamaPullUrl = computed(() =>
  convertToOllamaUrl(LLM_HUGGINGFACE_REPO, LLM_HUGGINGFACE_FILE)
);
async function checkModelAvailable(next?: () => void) {
  isModelAvailable.value = await sendMessage(
    "checkIsModelAvailable",
    ollamaPullUrl.value
  );
  if (isModelAvailable.value) {
    if (next) {
      next();
    }
  }
}
const modelStepTitle = computed(() => {
  let suffix = " ";
  if (isModelAvailable.value === true) {
    suffix = " (Modell gefunden)";
  } else if (modelStepInteracted.value === true) {
    suffix = " (Modell nicht gefunden)";
  }
  return `KI-Modell herunterladen${suffix}`;
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
  let suffix = "";
  if (isPinned.value) {
    suffix = " (angeheftet)";
  } else {
    suffix = " (optional)";
  }
  return `Browsererweiterung anheften${suffix}`;
});
</script>
