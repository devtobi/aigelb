import { i18n } from "#i18n";
import { Browser } from "@wxt-dev/browser";
import getUILanguage = Browser.i18n.getUILanguage;

export function setDocumentTitleByKey(key: string) {
  // @ts-expect-error-next-line - i18n.t does not expose union type
  const title = i18n.t(key);
  if (typeof title === "string" && title.length > 0) {
    document.title = title;
  }
}

export function applyLocaleToHtmlLang() {
  document.documentElement.lang = getUILanguage?.() ?? "en";
}
