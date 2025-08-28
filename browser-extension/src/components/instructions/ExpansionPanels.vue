<template>
  <v-expansion-panels model-value="0">
    <setup-card @onboarding-completed-changed="onBoardingCompletedChanged" />
    <uninstall-card />
    <links-card />
  </v-expansion-panels>
</template>

<script setup lang="ts">
import LinksCard from "@/components/instructions/LinksCard.vue";
import SetupCard from "@/components/instructions/SetupCard.vue";
import UninstallCard from "@/components/instructions/UninstallCard.vue";

const emit = defineEmits<{
  onboardingCompletedChanged: [value: boolean];
}>();

function onBoardingCompletedChanged(value: boolean) {
  emit("onboardingCompletedChanged", value);
}
</script>
