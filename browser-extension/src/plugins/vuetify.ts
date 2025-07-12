import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi-svg";

import "unfonts.css";
// @ts-expect-error: "TS2307 cannot find module" is a false positive here
import "vuetify/styles";
import "@/styles/override.css";

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
});
