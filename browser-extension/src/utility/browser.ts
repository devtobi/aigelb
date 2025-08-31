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

export async function setErrorBadge() {
  browser.action.setBadgeBackgroundColor({ color: "red" });
  browser.action.setBadgeTextColor({ color: "white" });
  browser.action.setBadgeText({ text: "!" });
}

export async function clearErrorBadge() {
  browser.action.setBadgeText({ text: "" });
}

export async function getActiveTabId() {
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return null;
  return tab.id;
}

export function openInstructions() {
  browser.tabs?.create({
    url: browser.runtime.getURL("/instructions.html"),
  });
}
