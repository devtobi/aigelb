import { defineExtensionMessaging } from "@webext-core/messaging";

interface ProtocolMap {
  checkOllamaConnection(): boolean;
  checkIsModelAvailable(ollamaPullUrl: string): boolean;
  getModelSize(data: { repo: string; file: string }): number | null;
}

export const { sendMessage, onMessage } =
  defineExtensionMessaging<ProtocolMap>();
