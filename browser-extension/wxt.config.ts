import UnpluginFontsPlugin from "unplugin-fonts/vite";
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
      features: {
        optionsAPI: false,
      },
    },
  },
  vite: () => ({
    plugins: [
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
