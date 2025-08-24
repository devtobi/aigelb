import { createApp } from "vue";

import App from "@/entrypoints/onboarding/App.vue";
import { registerVuePlugins } from "@/plugins";

const app = createApp(App);

registerVuePlugins(app);

app.mount("#app");
