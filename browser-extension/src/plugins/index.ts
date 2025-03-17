import type { App } from "vue";

import vuetify from "@/plugins/vuetify";

export function registerVuePlugins(app: App) {
  app.use(vuetify);
}
