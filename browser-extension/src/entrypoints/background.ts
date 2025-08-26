import { defineBackground } from "#imports";

import registerHuggingFaceCommunication from "@/entrypoints/background/registerHuggingFaceCommunication.ts";
import registerOllamaCommunication from "@/entrypoints/background/registerOllamaCommunication.ts";
import registerOnboarding from "@/entrypoints/background/registerOnboarding.ts";
import registerNetworkingRules from "@/entrypoints/background/registerNetworkingRules.ts";

export default defineBackground(() => {
  registerNetworkingRules();
  registerOllamaCommunication();
  registerHuggingFaceCommunication();
  registerOnboarding();
});
