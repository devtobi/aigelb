import { load } from "cheerio";
import getXPath from "get-xpath";

export function isInsideElement(e: MouseEvent, element: HTMLElement | null) {
  return element
    ? (typeof (e as UIEvent).composedPath === "function" &&
        e.composedPath().includes(element)) ||
        (e.target instanceof Node && element.contains(e.target))
    : false;
}

export function elementContainsText(el: Element): boolean {
  try {
    const html = (el as HTMLElement).outerHTML ?? "";
    const $ = load(html);
    $("script, style, noscript, template").remove();
    const text = $.root().text();
    return text.trim().length > 0;
  } catch {
    // Fallback: minimal DOM-based check
    const t = (el as HTMLElement).innerText ?? "";
    return t.trim().length > 0;
  }
}

function getShadowHost(element: HTMLElement | null): HTMLElement | null {
  if (!element) return null;
  const root = element.getRootNode();
  return root instanceof ShadowRoot ? (root.host as HTMLElement) : null;
}

export function elementAtClientPoint(
  element: HTMLElement | null,
  x: number,
  y: number
): Element | null {
  const host = getShadowHost(element);
  const list = document.elementsFromPoint(x, y);
  for (const el of list) {
    if (!(el instanceof Element)) continue;
    if (host && el === host) continue;
    if (el === document.documentElement || el === document.body) continue;
    if (element && el instanceof Node && element.contains(el)) continue;
    return el;
  }
  return null;
}

export function getXPathForElement(element: Element | HTMLElement) {
  return getXPath(element);
}

function getElementByXPath(xPath: string) {
  const result = document.evaluate(
    xPath,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  );
  return result.singleNodeValue;
}

export function replaceElementByXPath(xPath: string, newElement: Node) {
  const oldEl = getElementByXPath(xPath);
  if (!oldEl || !oldEl.parentNode) {
    console.warn("Element not found or has no parent:", xPath);
    return;
  }
  oldEl.parentNode.replaceChild(newElement, oldEl);
}
