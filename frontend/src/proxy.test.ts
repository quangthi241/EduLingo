import { describe, it, expect } from "vitest";
import { NextRequest } from "next/server";
import { proxy } from "./proxy";

function req(pathname: string, cookie?: string) {
  const url = `http://localhost${pathname}`;
  const headers = new Headers();
  if (cookie) headers.set("cookie", cookie);
  return new NextRequest(url, { headers });
}

function makeJwt(payload: object): string {
  const header = "header";
  const encoded = btoa(JSON.stringify(payload))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  return `${header}.${encoded}.sig`;
}

describe("proxy", () => {
  it("allows /today with auth cookie", () => {
    const res = proxy(req("/today", "edu_jwt=abc"));
    expect(res.status).toBe(200);
  });

  it("redirects /today to /login without auth cookie", () => {
    const res = proxy(req("/today"));
    expect(res.status).toBe(307);
    expect(res.headers.get("location")).toMatch(/\/login\?next=%2Ftoday/);
  });

  it("protects /library as well", () => {
    const res = proxy(req("/library"));
    expect(res.status).toBe(307);
  });

  it("allows marketing landing /", () => {
    const res = proxy(req("/"));
    expect(res.status).toBe(200);
  });

  it("redirects /admin to /today for learner-role token", () => {
    const token = makeJwt({ sub: "x", role: "learner" });
    const res = proxy(req("/admin", `edu_jwt=${token}`));
    expect(res.status).toBe(307);
    expect(res.headers.get("location")).toMatch(/\/today$/);
  });

  it("allows /admin/content for admin-role token", () => {
    const token = makeJwt({ sub: "x", role: "admin" });
    const res = proxy(req("/admin/content", `edu_jwt=${token}`));
    expect(res.status).toBe(200);
  });
});
