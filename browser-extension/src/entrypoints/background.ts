import { browser } from "wxt/browser";
import { defineBackground } from "wxt/sandbox";

export default defineBackground({
	type: 'module',
	main() {
	  console.debug("Hello background!", { id: browser.runtime.id });
	},
});
