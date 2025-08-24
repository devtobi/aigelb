import { defineBackground } from "#imports";

import registerOnboarding from "@/entrypoints/background/registerOnboarding.ts";

export default defineBackground(() => {
  registerOnboarding();
});
