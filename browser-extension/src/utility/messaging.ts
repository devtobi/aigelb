import type { DownloadProgress } from "@/types/DownloadProgress.ts";

import { defineExtensionMessaging } from "@webext-core/messaging";

interface ProtocolMap {
  // Prerequisites checking
  checkOllamaConnection(): boolean;
  checkIsModelAvailable(ollamaPullUrl: string): boolean;
  // Model management
  downloadModel(ollamaPullUrl: string): void;
  deleteModel(ollamaPullUrl: string): boolean;
  downloadProgress(downloadProgress: DownloadProgress): void;
  getModelSize(data: { repo: string; file: string }): number | null;
  // DOM selection
  startSelection(): void;
  // Inference lifecycle and status
  checkIsInferenceRunning(): boolean;
  startInference(text: string): void;
}

export const { sendMessage, onMessage } =
  defineExtensionMessaging<ProtocolMap>();
