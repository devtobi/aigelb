import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi-svg";

import "@/styles/main.scss";

export default createVuetify({
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    themes: {
      light: {
        colors: {
          primary: "#FFA300",
          secondary: "#FFFFFF",
          accent: "#FFFFFF",
          success: "#69BE28",
          error: "#FF0000",
        },
      },
    },
  },
});
