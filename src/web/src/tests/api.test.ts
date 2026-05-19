import { setToken } from "../services/api";

test("setToken does not throw", () => {
  expect(() => setToken("abc")).not.toThrow();
});
