import { createApp } from "vue";

import { registerVuePlugins } from "@/plugins";

import "unfonts.css";

import App from "@/entrypoints/popup/App.vue";

const app = createApp(App);

registerVuePlugins(app);

app.mount("#app");
