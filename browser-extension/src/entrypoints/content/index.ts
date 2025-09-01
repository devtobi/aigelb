import type { ContentScriptContext } from "wxt/utils/content-script-context";

import { defineContentScript } from "#imports";
import { createApp } from "vue";
import { createShadowRootUi } from "wxt/utils/content-script-ui/shadow-root";

import App from "@/entrypoints/content/App.vue";
import { registerVuePlugins } from "@/plugins";

export default defineContentScript({
  matches: ["*://*/*"],
  cssInjectionMode: "ui",
  async main(context: ContentScriptContext) {
    const ui = await createShadowRootUi(context, {
      name: "aigelb-ui",
      isolateEvents: true,
      position: "overlay",
      anchor: "body",
      onMount: (container) => {
        const app = createApp(App);
        registerVuePlugins(app);
        app.mount(container);
        return app;
      },
      onRemove: (app) => {
        app?.unmount();
      },
    });

    const notifyInvalidated = () => {
      ui.remove();
    };
    context.onInvalidated(notifyInvalidated);

    ui.mount();
  },
});
