import { defineContentScript } from "#imports";
import type { ContentScriptContext } from "wxt/utils/content-script-context";
import { createApp } from "vue";
import App from "@/entrypoints/content/App.vue";
import { createShadowRootUi } from "wxt/utils/content-script-ui/shadow-root";
import { registerVuePlugins } from "@/plugins";

export default defineContentScript({
  matches: ["*://*/*"],
  cssInjectionMode: "ui",
  async main(context: ContentScriptContext) {
    const ui = await createShadowRootUi(context, {
      name: 'aigelb-ui',
      isolateEvents: true,
      position: 'inline',
      anchor: 'body',
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

    context.onInvalidated(() => {
      console.debug("Content script got invalidated.");
    });
    ui.mount();
  }
});
