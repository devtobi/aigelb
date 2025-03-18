import { storage } from "@wxt-dev/storage";
import { beforeEach, describe, expect, it } from "vitest";
import { fakeBrowser } from "wxt/testing";

interface TestStorageItem {
  content: string;
}

const testStorage = storage.defineItem<TestStorageItem>("local:testkey");

async function hasTestStorageKey(): Promise<boolean> {
  const value = await testStorage.getValue();
  return value != null;
}

describe("Background dummy entrypoint tests", () => {
  beforeEach(() => {
    fakeBrowser.reset();
  });

  it("should return true when the test item exists in storage", async () => {
    const item: TestStorageItem = {
      content: "dummy-content",
    };
    await testStorage.setValue(item);
    expect(await hasTestStorageKey()).toBe(true);
  });

  it("should return false when the test item does not exist in storage", async () => {
    await testStorage.removeValue();
    expect(await hasTestStorageKey()).toBe(false);
  });
});
