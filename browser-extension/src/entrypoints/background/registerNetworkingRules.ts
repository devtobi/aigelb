import { browser } from "wxt/browser";

import { removeOriginUsingDeclarativeWebRequest } from "@/utility/networking.ts";

export default function registerNetworkingRules() {
  browser.runtime.onInstalled.addListener(async () => {
    await removeOriginUsingDeclarativeWebRequest();
  });
}
