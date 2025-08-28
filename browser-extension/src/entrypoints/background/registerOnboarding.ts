import type { Browser } from "wxt/browser";

import { browser } from "wxt/browser";

import { openInstructions } from "@/utility/browser.ts";

export default function registerOnboarding() {
  browser.runtime.onInstalled?.addListener(
    (details: Browser.runtime.InstalledDetails) => {
      if (details.reason === browser.runtime.OnInstalledReason?.INSTALL) {
        openInstructions();
      }
    }
  );
}
