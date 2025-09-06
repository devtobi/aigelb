import type { ContentScriptContext } from "wxt/utils/content-script-context";

import { defineContentScript } from "#imports";
import { createApp } from "vue";
import { createShadowRootUi } from "wxt/utils/content-script-ui/shadow-root";

import App from "@/entrypoints/content/App.vue";
import { registerVuePlugins } from "@/plugins";
import { syncCSSStyleSheets } from "@/utility/css.ts";

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

        const root = container.getRootNode();
        if (root instanceof ShadowRoot) {
          const STYLE_ID = "vuetify-theme-stylesheet";

          const themeSheet = new CSSStyleSheet();

          void syncCSSStyleSheets(STYLE_ID, themeSheet, root);

          const headObserver = new MutationObserver(() => {
            void syncCSSStyleSheets(STYLE_ID, themeSheet, root);
          });
          headObserver.observe(document.head, {
            childList: true,
            subtree: true,
            characterData: true,
          });
        }
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
