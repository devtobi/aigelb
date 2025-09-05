export type InferenceStatus = "generating" | "completed" | "error";

export interface InferenceProgress {
  text: string;
  status: InferenceStatus;
}
