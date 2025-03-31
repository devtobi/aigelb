import { defineContentScript } from "#imports";

export default defineContentScript({
  matches: ["*://*.google.com/*"],
  main() {
    console.debug("Hello content.");
  },
});
