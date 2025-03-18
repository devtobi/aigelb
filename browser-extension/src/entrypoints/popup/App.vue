<template>
  <v-app style="width: 800px">
    <v-container>
      <v-btn
        :prepend-icon="mdiAccessPoint"
        @click="sendMessageTest"
        >{{ i18n.t("helloWorld") }}</v-btn
      >
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { mdiAccessPoint } from "@mdi/js";
import { i18n } from "#i18n";
import { VApp, VBtn, VContainer } from "vuetify/components";
import { sendMessage } from "webext-bridge/popup";

import { TestEventName } from "@/types/TestEvent.ts";

async function sendMessageTest() {
  const response = await sendMessage(
    TestEventName,
    {
      message: "hello world",
    },
    "background"
  );
  console.debug(response);
}
</script>
