import type { RepoDesignation } from "@huggingface/hub";

import { listFiles } from "@huggingface/hub";

export async function getModelSize(repo: string, file: string) {
  const repository: RepoDesignation = { type: "model", name: repo };
  try {
    const files = listFiles({ repo: repository, recursive: true });
    for await (const fileEntry of files) {
      if (fileEntry.path.endsWith(file)) {
        return fileEntry.size;
      }
    }
    return null;
  } catch (error: unknown) {
    console.debug(
      `HuggingFace model size retrieval failed: ${error instanceof Error ? error.message : String(error)}`
    );
    return null;
  }
}
