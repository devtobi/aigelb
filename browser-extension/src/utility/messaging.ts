import { defineExtensionMessaging } from "@webext-core/messaging";

interface ProtocolMap {
  testEvent(content: string): number;
}

export const { sendMessage, onMessage } =
  defineExtensionMessaging<ProtocolMap>();
