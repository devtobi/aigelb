export type InferenceStatus = "generating" | "completed" | "error";

export interface InferenceProgress {
  generationId: string;
  status: InferenceStatus;
  text: string;
}
