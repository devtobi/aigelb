export type DownloadStatus = "downloading" | "completed" | "error";

export interface DownloadProgress {
  percentage: number;
  status: DownloadStatus;
}
