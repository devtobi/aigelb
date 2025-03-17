import { defineContentScript } from "wxt/sandbox";

export default defineContentScript({
  matches: ["*://*.google.com/*"],
  main() {
    console.debug("Hello content.");
  },
});
