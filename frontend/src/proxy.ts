import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const PROTECTED_PATTERNS: RegExp[] = [
  /^\/today/,
  /^\/library/,
  /^\/review/,
  /^\/progress/,
  /^\/session/,
  /^\/profile/,
  /^\/onboarding/,
  /^\/placement(-intro)?/,
  /^\/admin/,
];

const ADMIN_PATTERN = /^\/admin(\/|$)/;

const COOKIE_NAME = "edu_jwt";

function decodeRole(token: string): string | null {
  const [, payload] = token.split(".");
  if (!payload) return null;
  try {
    const padded = payload.replace(/-/g, "+").replace(/_/g, "/");
    const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
    const json = atob(padded + pad);
    const claims = JSON.parse(json) as { role?: string };
    return claims.role ?? null;
  } catch {
    return null;
  }
}

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isProtected = PROTECTED_PATTERNS.some((p) => p.test(pathname));
  if (!isProtected) {
    return NextResponse.next();
  }
  const token = request.cookies.get(COOKIE_NAME)?.value;
  if (!token) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  if (ADMIN_PATTERN.test(pathname)) {
    const role = decodeRole(token);
    if (role !== "admin") {
      const url = request.nextUrl.clone();
      url.pathname = "/today";
      url.search = "";
      return NextResponse.redirect(url);
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next|api|favicon|.*\\..*).*)"],
};
