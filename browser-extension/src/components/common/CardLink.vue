<template>
  <v-card
    :title="title"
    :subtitle="subtitle"
    :href="link"
    :append-icon="link ? mdiOpenInNew : ''"
    :prepend-icon="icon"
    v-bind="linkAttributes"
    flat
  />
</template>

<script setup lang="ts">
import { mdiOpenInNew } from "@mdi/js";
import { computed } from "vue";

const props = defineProps<{
  title: string;
  subtitle?: string;
  icon?: string;
  link?: string;
}>();

const linkAttributes = computed(() =>
  props.link ? { href: props.link, target: "_blank", rel: "noopener" } : {}
);
</script>
