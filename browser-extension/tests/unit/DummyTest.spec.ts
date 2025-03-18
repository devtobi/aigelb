import { describe, expect, it } from "vitest";

describe("DummyTest", () => {
  it("should add the correct sum for 2 + 2", () => {
    // when
    const result = 2 + 2;

    // then
    expect(result).toBe(4);
  });
});
