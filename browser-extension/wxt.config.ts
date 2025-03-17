import UnpluginFontsPlugin from "unplugin-fonts/vite";
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
import { defineConfig } from "wxt";

// See https://wxt.dev/api/config.html
export default defineConfig({
  extensionApi: "chrome",
  modules: ["@wxt-dev/auto-icons", "@wxt-dev/module-vue"],
  srcDir: "src",
  outDir: "dist",
  manifest: ({ manifestVersion }) => ({
    permissions: [],
    host_permissions: manifestVersion === 2 ? [] : [],
  }),
  runner: {
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
  vite: () => ({
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
  }),
});
