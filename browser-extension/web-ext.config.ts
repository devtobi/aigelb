import { defineRunnerConfig } from "wxt";

export default defineRunnerConfig({
  binaries: {
    chrome: "/Applications/Chromium.app/Contents/MacOS/Chromium",
    firefox: "firefoxdeveloperedition",
  },
  chromiumArgs: ["--user-data-dir=./.wxt/chrome-data"],
});
