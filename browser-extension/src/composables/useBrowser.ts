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

  return {
    openOptionsPage,
    closeWindow,
    getUILanguage,
  };
}
