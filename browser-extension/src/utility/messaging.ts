import type { DownloadProgress } from "@/types/DownloadProgress.ts";
import type { InferenceData } from "@/types/InferenceData.ts";
import type { InferenceProgress } from "@/types/InferenceProgress.ts";
import type { ModelData } from "@/types/ModelData.ts";

import { defineExtensionMessaging } from "@webext-core/messaging";

interface ProtocolMap {
  // Prerequisites checking
  checkOllamaConnection(): boolean;
  checkIsModelAvailable(ollamaPullUrl: string): boolean;
  // Model management
  downloadModel(ollamaPullUrl: string): void;
  deleteModel(ollamaPullUrl: string): boolean;
  downloadProgress(downloadProgress: DownloadProgress): void;
  getModelSize(data: ModelData): number | null;
  // DOM selection
  startSelection(): void;
  // Inference lifecycle and status
  checkIsInferenceRunning(): boolean;
  startInference(data: InferenceData): void;
  abortInference(): void;
  inferenceProgress(inferenceProgress: InferenceProgress): void;
}

export const { sendMessage, onMessage } =
  defineExtensionMessaging<ProtocolMap>();
