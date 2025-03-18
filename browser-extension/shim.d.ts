import type { TestEventPayload, TestEventResponse } from "@/types/TestEvent.ts";

import { ProtocolWithReturn } from "webext-bridge";

import { TestEventName } from "@/types/TestEvent.ts";

declare module "webext-bridge" {
  export interface ProtocolMap {
    [TestEventName]: ProtocolWithReturn<TestEventPayload, TestEventResponse>;
  }
}
