<template>
  <v-app>
    <the-app-bar />

    <v-main>
      <v-container class="fill-height">
        <v-row
          align="end"
          class="mx-1 fill-height"
        >
          <instructions-button />
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import TheAppBar from "@/components/common/TheAppBar.vue";
import InstructionsButton from "@/components/popup/InstructionsButton.vue";
</script>

<style>
body {
  min-width: 320px;
  max-width: 480px;
  height: 400px;
}
</style>
