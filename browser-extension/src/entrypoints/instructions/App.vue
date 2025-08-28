<template>
  <v-app>
    <close-dialog
      :show="showDialog"
      @close="confirmedClose"
      @cancel="cancelClose"
    />
    <the-app-bar />

    <v-main>
      <v-container>
        <header-card class="mb-8" />
        <about-card class="mb-8" />
        <important-notes-card class="mb-8" />
        <setup-card
          class="mb-8"
          @onboarding-completed-changed="onOnboardingCompletedChanged"
        />
        <links-panel class="mb-8" />
        <close-button @close="onClickClose" />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

import TheAppBar from "@/components/common/TheAppBar.vue";
import AboutCard from "@/components/instructions/AboutCard.vue";
import CloseButton from "@/components/instructions/CloseButton.vue";
import CloseDialog from "@/components/instructions/CloseDialog.vue";
import HeaderCard from "@/components/instructions/HeaderCard.vue";
import ImportantNotesCard from "@/components/instructions/ImportantNotesCard.vue";
import LinksPanel from "@/components/instructions/LinksPanel.vue";
import SetupCard from "@/components/instructions/SetupCard.vue";
import { useBrowser } from "@/composables/useBrowser.ts";

const { closeWindow } = useBrowser();

const showDialog = ref(false);

const isOnboardingCompleted = ref(false);

function onOnboardingCompletedChanged(value: boolean) {
  isOnboardingCompleted.value = value;
}

function onClickClose() {
  if (!isOnboardingCompleted.value) {
    showDialog.value = true;
  } else {
    closeWindow();
  }
}

function confirmedClose() {
  showDialog.value = false;
  removeBeforeUnload();
  closeWindow();
}

function cancelClose() {
  showDialog.value = false;
}

function beforeUnloadHandler(event: BeforeUnloadEvent) {
  if (!isOnboardingCompleted.value) {
    event.preventDefault();
  } else {
    removeBeforeUnload();
  }
}

function removeBeforeUnload() {
  window.removeEventListener("beforeunload", beforeUnloadHandler);
}

onMounted(() => {
  window.addEventListener(
    "click",
    () => {
      window.addEventListener("beforeunload", beforeUnloadHandler);
    },
    { once: true }
  );
});

onBeforeUnmount(() => {
  removeBeforeUnload();
});
</script>
