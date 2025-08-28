import { i18n } from "#i18n";

import { useBrowser } from "@/composables/useBrowser.ts";

export function setDocumentTitleByKey(key: string) {
  // @ts-expect-error-next-line - i18n.t does not expose union type
  const title = i18n.t(key);
  if (typeof title === "string" && title.length > 0) {
    document.title = title;
  }
}

export function applyLocaleToHtmlLang() {
  const { getUILanguage } = useBrowser();
  document.documentElement.lang = getUILanguage?.() ?? "en";
}
