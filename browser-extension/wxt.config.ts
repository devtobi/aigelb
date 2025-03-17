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
    host_permissions: [],
    author:
      manifestVersion === 3
        ? {
            email: "devtobi - Tobias Stadler",
          }
        : "devtobi - Tobias Stadler",
    name: "AIGELB - AI German Easy Language Browsing",
    short_name: "AIGELB",
    homepage_url: "https://github.com/devtobi/aigelb",
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
  autoIcons: {
    grayscaleOnDevelopment: false,
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
