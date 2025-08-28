import { browser } from "wxt/browser";

export function closeWindow() {
  window.close();
}

export function getUILanguage() {
  return browser.i18n?.getUILanguage();
}

export async function isPinnedInToolbar() {
  const userSettings = browser.action?.getUserSettings
    ? await browser.action?.getUserSettings()
    : undefined;
  if (!userSettings) return true;
  return !!userSettings.isOnToolbar;
}

export function openInstructions() {
  browser.tabs?.create({
    url: browser.runtime.getURL("/instructions.html"),
  });
}
