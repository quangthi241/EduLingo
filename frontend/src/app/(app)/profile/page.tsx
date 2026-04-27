"use client";

import Link from "next/link";
import { useState } from "react";

import { Section } from "@shared/ui/Card";
import { ThemeToggle } from "@shared/ui/ThemeToggle";
import { Button } from "@shared/ui/Button";

function decodeJwtRole(token: string | null): string | null {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length < 2) return null;
  try {
    const padded = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
    const json = atob(padded + pad);
    const claims = JSON.parse(json) as { role?: string };
    return claims.role ?? null;
  } catch {
    return null;
  }
}

function readCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.slice(name.length + 1)) : null;
}

export default function ProfilePage() {
  const [role] = useState<string | null>(() => decodeJwtRole(readCookie("edu_jwt")));

  return (
    <div className="mx-auto flex max-w-[68ch] flex-col gap-10">
      <header className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          Account
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-4xl font-semibold tracking-tight">
          Profile
        </h1>
        {role === "admin" && (
          <Link
            href="/admin"
            className="mt-3 inline-flex items-center gap-2 text-sm text-accent hover:underline"
          >
            Go to admin →
          </Link>
        )}
      </header>
      <Section eyebrow="Appearance" heading="Theme">
        <ThemeToggle />
      </Section>
      <Section eyebrow="Account" heading="Sign out">
        <Button
          variant="ghost"
          onClick={() => {
            document.cookie = "edu_jwt=; Max-Age=0; path=/";
            window.location.assign("/");
          }}
        >
          Sign out
        </Button>
      </Section>
    </div>
  );
}
