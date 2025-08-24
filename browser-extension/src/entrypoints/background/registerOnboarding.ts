import type { Browser } from "wxt/browser";

import { browser } from "wxt/browser";

export default function registerOnboarding() {
  browser.runtime.onInstalled.addListener(
    (details: Browser.runtime.InstalledDetails) => {
      if (details.reason === browser.runtime.OnInstalledReason.INSTALL) {
        // Open onboarding page when extension is installed
        browser.tabs.create({
          url: browser.runtime.getURL("onboarding.html"),
        });
      }
    }
  );
}
