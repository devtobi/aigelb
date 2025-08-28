import { filesize } from "filesize";

export function convertFileSize(sizeInBytes: number) {
  return filesize(sizeInBytes);
}

export function convertToOllamaUrl(repo: string, file: string) {
  const quantization = file.split("-").pop()?.replace(".gguf", "");
  if (quantization) {
    return `hf.co/${repo}:${quantization}`;
  }
  throw Error("Quantization not found in file name");
}
