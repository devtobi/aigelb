<template>
  <v-img
    :width="size"
    aspect-ratio="1/1"
    cover
    :src="logo"
  />
</template>

<script setup lang="ts">
import logo from "@/assets/icon.png";

const { size = 64 } = defineProps<{
  size?: number;
}>();
</script>
