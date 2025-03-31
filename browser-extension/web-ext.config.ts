import { defineWebExtConfig } from "wxt";

export default defineWebExtConfig({
  binaries: {
    chrome: "/Applications/Chromium.app/Contents/MacOS/Chromium",
    firefox: "firefoxdeveloperedition",
  },
  chromiumArgs: ["--user-data-dir=./.wxt/chrome-data"],
});
