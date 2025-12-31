import { describe, it, expect } from "vitest";

describe("Basic tests", () => {
  it("should pass basic assertion", () => {
    expect(1 + 1).toBe(2);
  });

  it("should work with arrays", () => {
    const arr = [1, 2, 3];
    expect(arr).toContain(2);
    expect(arr).toHaveLength(3);
  });

  it("should work with objects", () => {
    const obj = { name: "test", value: 42 };
    expect(obj).toHaveProperty("name", "test");
    expect(obj.value).toBeGreaterThan(40);
  });
});
