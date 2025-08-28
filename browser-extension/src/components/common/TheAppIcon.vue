<template>
  <v-img
    :width="size"
    :height="size"
    cover
    :src="logo"
    :transition="false"
  />
</template>

<script setup lang="ts">
import logo from "@/assets/icon.png";

const { size = 64 } = defineProps<{
  size?: number;
}>();
</script>
