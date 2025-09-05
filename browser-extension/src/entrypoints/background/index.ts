import { defineBackground } from "#imports";

import registerHuggingFaceCommunication from "@/entrypoints/background/registerHuggingFaceCommunication.ts";
import registerNetworkingRules from "@/entrypoints/background/registerNetworkingRules.ts";
import registerOllamaCommunication from "@/entrypoints/background/registerOllamaCommunication.ts";
import registerOnboarding from "@/entrypoints/background/registerOnboarding.ts";
import registerInference from "@/entrypoints/background/registerInference.ts";

export default defineBackground(() => {
  registerNetworkingRules();
  registerOllamaCommunication();
  registerHuggingFaceCommunication();
  registerOnboarding();
  registerInference();
});
