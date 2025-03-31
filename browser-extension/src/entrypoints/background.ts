import { defineBackground } from "#imports";
import { onMessage } from "webext-bridge/background";

import { TestEventName } from "@/types/TestEvent.ts";

export default defineBackground({
  type: "module",
  main() {
    onMessage(TestEventName, (bridgeMessage) => {
      console.debug(bridgeMessage);
      return {
        length: bridgeMessage.data.message.length,
      };
    });
  },
});
