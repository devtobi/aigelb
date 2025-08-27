<template>
  <v-app>
    <the-app-bar />

    <v-main>
      <v-container>
        <header-card class="mb-8" />
        <about-card class="mb-8" />
        <important-notes-card class="mb-8" />
        <setup-card class="mb-8" />
        <links-panel class="mb-8" />
        <close-button @close="closeWindow" />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import TheAppBar from "@/components/common/TheAppBar.vue";
import AboutCard from "@/components/instructions/AboutCard.vue";
import CloseButton from "@/components/instructions/CloseButton.vue";
import HeaderCard from "@/components/instructions/HeaderCard.vue";
import ImportantNotesCard from "@/components/instructions/ImportantNotesCard.vue";
import LinksPanel from "@/components/instructions/LinksPanel.vue";
import SetupCard from "@/components/instructions/SetupCard.vue";
import { useBrowser } from "@/composables/useBrowser.ts";

const { closeWindow } = useBrowser();
</script>
