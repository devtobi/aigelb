<template>
  <v-stepper-vertical v-model="currentStep">
    <template #default>
      <v-stepper-vertical-item
        :title="ollamaStepTitle"
        value="1"
        :complete="isOllamaAvailable"
        elevation="0"
        :error="isOllamaAvailable === false"
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
          Ollama muss während der Nutzung von AIGELB im Hintergrund ausgeführt
          werden, damit die Browsererweiterung funktioniert. Je nach
          Betriebssystem muss Ollama z.B. nach dem Systemstart manuell gestartet
          werden.
        </v-alert>

        <template #next="{ next }">
          <v-btn
            :color="isOllamaAvailable === false ? 'error' : 'warning'"
            @click="checkOllamaConnection(next)"
          >
            {{ isOllamaAvailable === false ? "Erneut versuchen" : "Weiter" }}
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
        :error="isModelAvailable === false"
      >
        <p>TODO</p>
        <template #next="{ next }">
          <v-btn
            :color="isModelAvailable === false ? 'error' : 'warning'"
            @click="checkModelAvailable(next)"
          >
            {{ isModelAvailable === false ? "Erneut versuchen" : "Weiter" }}
          </v-btn>
        </template>
        <template v-slot:prev>
          <model-download-button
            :disabled="isModelAvailable === true"
            :repo="LLM_HUGGINGFACE_REPO"
            :file="LLM_HUGGINGFACE_FILE"
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
          Für die einfache Nutzung der Browsererweiterung sollte diese über die
          Browserleiste fest angeheftet werden.
        </p>

        <p>
          Eine Anleitung hierzu ist auf den Hilfe-Seiten des Browsers zu finden.
        </p>

        <template #next="{ next }">
          <v-btn
            color="warning"
            @click="next"
          />
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
          Bitte lies dir als Nächstes die Anleitung zur Nutzung der Erweiterung
          durch.
        </p>
      </v-stepper-vertical-item>
    </template>
  </v-stepper-vertical>
</template>

<script setup lang="ts">
import { mdiDownload } from "@mdi/js";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { VAlert, VBtn } from "vuetify/components";
import {
  VStepperVertical,
  VStepperVerticalItem,
} from "vuetify/labs/VStepperVertical";
import { browser } from "wxt/browser";

import ModelDownloadButton from "@/components/onboarding/ModelDownloadButton.vue";
import { useBrowser } from "@/composables/useBrowser.ts";
import { LLM_HUGGINGFACE_FILE, LLM_HUGGINGFACE_REPO } from "@/config.ts";
import { convertToOllamaUrl } from "@/utility/conversion.ts";
import { sendMessage } from "@/utility/messaging.ts";

onMounted(async () => {
  await updatePinStatus();
  await checkOllamaConnection();
  await checkModelAvailable();
  browser.action.onUserSettingsChanged?.addListener(updatePinStatus);
  jumpToFirstUncompletedStep();
});

const currentStep = ref(1);
function jumpToFirstUncompletedStep() {
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
  switch (isPinned.value) {
    case true:
      return "Browsererweiterung anheften (angeheftet)";
    default:
      return "Browsererweiterung anheften (optional)";
  }
});

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
  switch (isOllamaAvailable.value) {
    case true:
      return "KI-Software installieren (Verbindung erfolgreich)";
    case false:
      return "KI-Software installieren (Verbindung fehlgeschlagen)";
    default:
      return "KI-Software installieren";
  }
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
  switch (isModelAvailable.value) {
    case true:
      return "KI-Modell herunterladen (Modell gefunden)";
    case false:
      return "KI-Modell herunterladen (Modell nicht gefunden)";
    default:
      return "KI-Modell herunterladen";
  }
});
</script>
