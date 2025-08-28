import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi-svg";

import "unfonts.css";
// @ts-expect-error: "TS2307 cannot find module" is a false positive here
import "vuetify/styles";
import "@/styles/override.css";

import { de, en } from "vuetify/locale";

import { mapLangToVuetify } from "@/utility/i18n.ts";
import { Browser } from "@wxt-dev/browser";
import getUILanguage = Browser.i18n.getUILanguage;

const uiLanguage = mapLangToVuetify(getUILanguage());

export default createVuetify({
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: "system",
  },
  locale: {
    locale: uiLanguage,
    fallback: "de",
    messages: { de, en },
  },
});
