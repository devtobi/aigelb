import { existsSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

import { addAlias, defineWxtModule } from "wxt/modules";

export default defineWxtModule({
  setup(wxt) {
    const runtimeFile = "i18n/locales.ts";
    const declFile = "types/locales.d.ts";

    wxt.hook("prepare:types", (_, entries) => {
      const srcLocalesDir = resolve(wxt.config.srcDir, "locales");
      const codes = existsSync(srcLocalesDir)
        ? readdirSync(srcLocalesDir, { withFileTypes: true })
            .filter(
              (f) => f.isFile() && /\.(ya?ml|jsonc?|json5|toml)$/i.test(f.name)
            )
            .map((f) => f.name.replace(/\.(ya?ml|jsonc?|json5|toml)$/i, ""))
        : [];

      entries.push({
        path: runtimeFile,
        text:
          `export const supportedLanguages = ` +
          `${JSON.stringify([...new Set(codes)])} as const;`,
      });

      entries.push({
        path: declFile,
        text: `declare module "#locales" { export const supportedLanguages: readonly string[] }`,
        tsReference: true,
      });
    });

    addAlias(wxt, "#locales", ".wxt/" + runtimeFile);
  },
});
