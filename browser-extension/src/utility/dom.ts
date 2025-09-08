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

export function collectTextNodes(root: Element): Text[] {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      const p = (n as Text).parentElement;
      if (isIncompatibleParent(p)) return NodeFilter.FILTER_REJECT;
      if (isVisuallyHidden(p)) return NodeFilter.FILTER_REJECT;
      if (isEmptyTextContent(n)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const textNodes: Text[] = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode())
    textNodes.push(n as Text);
  return textNodes;
}

function isIncompatibleParent(el: Element | null): boolean {
  if (!el) return true;
  if (el.matches("script,style,noscript,code,pre,iframe")) return true;
  if ((el as HTMLElement).isContentEditable) return true;
  return false;
}

function isVisuallyHidden(el: Element | null): boolean {
  for (let cur: Element | null = el; cur; cur = cur.parentElement) {
    const current = cur as HTMLElement;

    if (current.hidden) return true;
    if (current.getAttribute("aria-hidden") === "true") return true;
    if (current.inert) return true;

    const style = window.getComputedStyle(cur);
    if (
      style.display === "none" ||
      style.visibility === "hidden" ||
      style.visibility === "collapse" ||
      style.opacity === "0"
    ) {
      return true;
    }
  }
  return false;
}

function isEmptyTextContent(node: Node | null): boolean {
  const text = node?.nodeValue?.trim();
  return !text;
}
