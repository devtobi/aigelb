import { browser } from "wxt/browser";
import { removeOrigin } from "@/utility/networking.ts";

export default function registerNetworkingRules() {
  browser.runtime.onInstalled.addListener(async () => {
    await removeOrigin();
  })
}
