export async function syncCSSStyleSheets(
  stylesheetId: string,
  themeSheet: CSSStyleSheet,
  root: ShadowRoot
) {
  const headStyle = document.getElementById(
    stylesheetId
  ) as HTMLStyleElement | null;
  if (!headStyle) return;
  const css = headStyle.textContent ?? "";
  if ("replaceSync" in themeSheet) {
    themeSheet.replaceSync(css);
  }
  const sheets = root.adoptedStyleSheets ?? [];
  if (!sheets.includes(themeSheet)) {
    root.adoptedStyleSheets = [...sheets, themeSheet];
  }
}
