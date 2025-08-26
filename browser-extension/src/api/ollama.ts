import ollama from "ollama/browser";

export async function isAvailable() {
  try {
    await ollama.list();
    return true;
  } catch (error: unknown) {
    console.debug(
      `Ollama health check failed: ${error instanceof Error ? error.message : String(error)}`
    );
    return false;
  }
}

export async function isModelAvailable(ollamaPullUrl: string) {
  try {
    const response = await ollama.list();
    const models = response.models.map((modelResponse) => modelResponse.name);
    return models.includes(ollamaPullUrl);
  } catch (error: unknown) {
    console.debug(
      `Listing downloaded models failed: ${error instanceof Error ? error.message : String(error)}`
    );
    return false;
  }
}

export async function downloadModel(ollamaPullUrl: string) {
  try {
    return await ollama.pull({
      model: ollamaPullUrl,
      stream: true,
    });
  } catch (error: unknown) {
    console.debug(
      `Downloading model from ${ollamaPullUrl} failed: ${error instanceof Error ? error.message : String(error)}`
    );
  }
}
