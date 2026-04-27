"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "./navigation";
import { ThemeToggle } from "@shared/ui/ThemeToggle";

export function TopNav() {
  const pathname = usePathname();
  return (
    <header className="hidden border-b border-[color:var(--color-border-strong)] md:block">
      <div className="mx-auto flex max-w-[76rem] items-end gap-10 px-10 pt-7 pb-4">
        <Link
          href="/today"
          aria-label="EduLingo home"
          className="flex items-baseline gap-2 no-underline"
        >
          <span className="font-display text-[1.7rem] font-semibold leading-none tracking-tight text-[color:var(--color-ink)]">
            EduLingo
          </span>
          <span className="eyebrow hidden lg:inline text-[color:var(--color-ink-subtle)]">
            &middot; Daily Brief
          </span>
        </Link>
        <nav aria-label="Primary" className="flex flex-1 items-baseline gap-7 pb-1">
          {NAV_ITEMS.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`relative text-sm font-medium transition-colors duration-150 [transition-timing-function:var(--ease-out-quart)] ${
                  active
                    ? "text-[color:var(--color-ink)]"
                    : "text-[color:var(--color-ink-muted)] hover:text-[color:var(--color-ink)]"
                }`}
              >
                <span>{item.label}</span>
                {active ? (
                  <span
                    aria-hidden
                    className="absolute -bottom-[17px] left-0 right-0 h-[2px] bg-[color:var(--color-accent)]"
                  />
                ) : null}
              </Link>
            );
          })}
        </nav>
        <div className="flex items-baseline gap-3 pb-1">
          <ThemeToggle />
          <Link
            href="/profile"
            aria-label="Profile"
            className="h-8 w-8 rounded-full border border-[color:var(--color-border)] bg-[color:var(--color-surface-sunken)] transition hover:border-[color:var(--color-ink)]"
          />
        </div>
      </div>
    </header>
  );
}
