import { defineBackground } from "#imports";

import { onMessage } from "@/utility/messaging";

export default defineBackground({
  type: "module",
  main() {
    onMessage("testEvent", (message) => {
      console.debug(`BACKGROUND - Received: ${message.data}`);
      return message.data.length;
    });
  },
});
