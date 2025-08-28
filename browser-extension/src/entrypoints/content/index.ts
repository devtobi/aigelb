import { defineContentScript } from "#imports";

export default defineContentScript({
  matches: ["*://*/*"],
  main() {
    console.debug("Hello from AIGELB.");
  },
});
