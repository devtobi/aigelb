import { browser } from "wxt/browser";

const RULE_ID_REMOVE_ORIGIN = 1;
const URL_FILTER = /https?:\/\/(localhost|127\.0\.0\.1):11434\//;

export async function removeOriginUsingDeclarativeWebRequest() {
  if (import.meta.env.FIREFOX) return;
  await browser.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: [RULE_ID_REMOVE_ORIGIN],
    addRules: [
      {
        id: RULE_ID_REMOVE_ORIGIN,
        priority: 1,
        action: {
          type: browser.declarativeNetRequest.RuleActionType.MODIFY_HEADERS,
          requestHeaders: [
            {
              header: "Origin",
              operation: browser.declarativeNetRequest.HeaderOperation.REMOVE,
            },
          ],
        },
        condition: {
          regexFilter: URL_FILTER.source,
          initiatorDomains: [browser.runtime.id],
          resourceTypes: [
            browser.declarativeNetRequest.ResourceType.XMLHTTPREQUEST,
          ],
        },
      },
    ],
  });
}
