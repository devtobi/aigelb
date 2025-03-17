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
      if (wxt.config.mode === "development") {
        manifest.name += " (DEV)";
      }
    },
  },
  imports: false,
  vue: {
    vite: {
	  features: {
	    optionsAPI: false
	  }
	}
  }
});
