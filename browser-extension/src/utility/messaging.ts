import type { DownloadProgress } from "@/types/DownloadProgress.ts";

import { defineExtensionMessaging } from "@webext-core/messaging";

interface ProtocolMap {
  checkOllamaConnection(): boolean;
  checkIsModelAvailable(ollamaPullUrl: string): boolean;
  downloadModel(ollamaPullUrl: string): void;
  deleteModel(ollamaPullUrl: string): boolean;
  downloadProgress(downloadProgress: DownloadProgress): void;
  getModelSize(data: { repo: string; file: string }): number | null;
  startSelection(): void;
}

export const { sendMessage, onMessage } =
  defineExtensionMessaging<ProtocolMap>();
