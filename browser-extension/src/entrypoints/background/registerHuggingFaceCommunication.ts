import { getModelSize } from "@/api/huggingface.ts";
import { onMessage } from "@/utility/messaging.ts";

export default function registerHuggingFaceCommunication() {
  onMessage("getModelSize", async (message) => {
    return await getModelSize(message.data.repo, message.data.file);
  });
}
