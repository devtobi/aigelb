import type {
  DownloadProgress,
  DownloadStatus,
} from "@/types/DownloadProgress.ts";

import {
  deleteModel,
  downloadModel,
  isAvailable,
  isModelAvailable,
} from "@/api/ollama.ts";
import { onMessage, sendMessage } from "@/utility/messaging.ts";

export default function registerOllamaCommunication() {
  onMessage("checkOllamaConnection", async () => {
    return await isAvailable();
  });
  onMessage("checkIsModelAvailable", async (message) => {
    return await isModelAvailable(message.data);
  });
  onMessage("downloadModel", async (message) => {
    try {
      const stream = await downloadModel(message.data);
      if (stream) {
        for await (const progress of stream) {
          let percentage;
          if (!progress.completed || !progress.total) {
            percentage = 0;
          } else {
            percentage = (progress.completed / progress.total) * 100;
          }
          let status: DownloadStatus;
          if (!progress.status || progress.status !== "success") {
            status = "downloading";
          } else {
            status = "completed";
            percentage = 100;
          }
          const downloadProgress: DownloadProgress = {
            percentage,
            status,
          };
          if (downloadProgress.percentage !== 0) {
            await sendMessage("downloadProgress", downloadProgress);
          }
        }
      }
    } catch (error: unknown) {
      console.debug(
        `Downloading model failed: ${error instanceof Error ? error.message : String(error)}`
      );
      await sendMessage("downloadProgress", {
        percentage: 0,
        status: "error",
      });
    }
  });
  onMessage("deleteModel", async (message) => {
    try {
      return await deleteModel(message.data);
    } catch (error: unknown) {
      console.debug(
        `Deleting model failed: ${error instanceof Error ? error.message : String(error)}`
      );
      return false;
    }
  });
}
