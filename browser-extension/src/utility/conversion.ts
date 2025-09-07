import { filesize } from "filesize";

const LINEARIZATION_PREFIX = "⟦N";
const LINEARIZATION_SUFFIX = "⟧";
export const LINEARIZATION_REGEX = new RegExp(`${LINEARIZATION_PREFIX}(\\d+)${LINEARIZATION_SUFFIX}`, "g");

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

export function linearizeTextNodesForInference(nodes: Text[]) {
  let s = "";
  nodes.forEach((t, i) => {
    s +=
      (t.nodeValue ?? "") +
      `${LINEARIZATION_PREFIX}${i}${LINEARIZATION_SUFFIX}`;
  });
  return s;
}
