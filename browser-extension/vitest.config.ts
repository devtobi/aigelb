import { defineConfig } from "vitest/config";
import { WxtVitest } from "wxt/testing";

export default defineConfig({
  test: {
    mockReset: true,
    restoreMocks: true,
    coverage: {
      exclude: ["./src/plugins", "./*.{ts,js}", ".wxt", "dist"],
    },
  },
  plugins: [WxtVitest()],
});
