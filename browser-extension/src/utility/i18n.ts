import { getUILanguage } from "@/utility/browser.ts";

export function mapLangToVuetify(locale: string) {
  if (locale.startsWith("de")) return "de";
  if (locale.startsWith("en")) return "en";
  return "de"; // fallback
}

export function getAssetUrl(filename: string): string {
  const lang = getUILanguage();
  const localizedHref = new URL(`../assets/${lang}/${filename}`, import.meta.url).href;
  if (localizedHref.indexOf("undefined") !== -1) {
    return new URL(`../assets/en/${filename}`, import.meta.url).href;
  }
  return localizedHref;
}
