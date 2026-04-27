"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "./navigation";

export function TabBar() {
  const pathname = usePathname();
  return (
    <nav
      aria-label="Primary"
      className="fixed inset-x-0 bottom-0 z-20 border-t border-[color:var(--color-border)] bg-[color:var(--color-surface)]/95 backdrop-blur md:hidden"
    >
      <ul className="flex">
        {NAV_ITEMS.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <li key={item.href} className="flex-1">
              <Link
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`flex flex-col items-center gap-0.5 px-2 py-2.5 text-[0.7rem] transition ${
                  active
                    ? "text-[color:var(--color-accent)]"
                    : "text-[color:var(--color-ink-subtle)]"
                }`}
              >
                <span aria-hidden className="text-base leading-none">
                  {item.glyph}
                </span>
                <span>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
