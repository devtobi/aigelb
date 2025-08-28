import { computed } from "vue";
import { browser } from "wxt/browser";

export function useManifestData() {
  const manifest = computed(() => browser.runtime.getManifest());
  const extensionName = computed(() => manifest.value.name);
  const extensionVersion = computed(() => manifest.value.version);

  return {
    extensionName,
    extensionVersion,
  };
}
