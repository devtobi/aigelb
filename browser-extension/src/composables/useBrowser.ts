import { browser } from "wxt/browser";

export function useBrowser() {
  function openOptionsPage() {
    browser.runtime.openOptionsPage();
  }

  function closeWindow() {
    window.close();
  }

  function getUILanguage() {
    return browser.i18n?.getUILanguage();
  }

  async function isPinnedInToolbar() {
    const userSettings = browser.action?.getUserSettings
      ? await browser.action?.getUserSettings()
      : undefined;
    if (!userSettings) return true;
    return !!userSettings.isOnToolbar;
  }

  return {
    openOptionsPage,
    closeWindow,
    getUILanguage,
    isPinnedInToolbar,
  };
}
