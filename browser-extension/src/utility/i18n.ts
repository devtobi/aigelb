export function mapLangToVuetify(locale: string) {
  if (locale.startsWith("de")) return "de";
  if (locale.startsWith("en")) return "en";
  return "de"; // fallback
}
