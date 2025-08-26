import type { WxtViteConfig } from "wxt";

import UnpluginFontsPlugin from "unplugin-fonts/vite";
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
import { defineConfig } from "wxt";

// See https://wxt.dev/api/config.html
export default defineConfig({
  modules: [
    "@wxt-dev/auto-icons",
    "@wxt-dev/module-vue",
    "@wxt-dev/i18n/module",
  ],
  srcDir: "src",
  outDir: "dist",
  targetBrowsers: ["chrome", "firefox", "safari"],
  manifest: ({ manifestVersion }) => ({
    author:
      manifestVersion === 3
        ? {
            email: "devtobi - Tobias Stadler",
          }
        : "devtobi - Tobias Stadler",
    name: "__MSG_manifestName__",
    short_name: "AIGELB",
    description: "__MSG_manifestDescription__",
    homepage_url: "https://github.com/devtobi/aigelb",
    default_locale: "de",
    permissions: [],
    host_permissions: [
      // Local Ollama URLs to connect to Ollama API
      "http://127.0.0.1:11434/*",
      "http://localhost:11434/*",
      // HuggingFace URLs to allow metadata retrieval
      "https://huggingface.co/*",
      "https://hf.co/*",
    ],
  }),
  webExt: {
    startUrls: ["http://localhost:8081"],
  },
  hooks: {
    "build:manifestGenerated": (wxt, manifest) => {
      if (wxt.config.mode !== "production") {
        manifest.name += ` (${wxt.config.mode})`;
      }
    },
  },
  imports: false,
  vue: {
    vite: {
      template: { transformAssetUrls },
      features: {
        optionsAPI: false,
      },
    },
  },
  autoIcons: {
    developmentIndicator: "overlay",
  },
  vite: () =>
    ({
      plugins: [
        vuetify({
          autoImport: false,
        }),
        UnpluginFontsPlugin({
          fontsource: {
            families: [
              {
                name: "Roboto",
                weights: [100, 300, 400, 500, 700, 900],
                subset: "latin",
              },
            ],
          },
        }),
      ],
    }) as WxtViteConfig,
});
