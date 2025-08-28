import { createApp } from "vue";

import App from "@/entrypoints/popup/App.vue";
import { registerVuePlugins } from "@/plugins";
import {
  applyLocaleToHtmlLang,
  setDocumentTitleByKey,
} from "@/utility/pageMeta.ts";

const app = createApp(App);

registerVuePlugins(app);

applyLocaleToHtmlLang();
setDocumentTitleByKey("pages.popup.title");

app.mount("#app");
