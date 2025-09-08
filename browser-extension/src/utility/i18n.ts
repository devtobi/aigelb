import type { PublicPath } from "wxt/browser";

import { supportedLanguages } from "#locales";
import { browser } from "wxt/browser";

import { getUILanguage } from "@/utility/browser.ts";

export function getImageUrl(filename: string): string {
  const lang = getUILanguage();
  const supported = new Set(supportedLanguages);
  const folder = supported.has(lang) ? lang : "en";
  return browser.runtime.getURL(`images/${folder}/${filename}` as PublicPath);
}
