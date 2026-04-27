"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface RailSection {
  label: string;
  items: { label: string; href: string }[];
}

const RAIL_BY_ROUTE: Record<string, RailSection[]> = {
  "/library": [
    {
      label: "Free practice",
      items: [
        { label: "Reading", href: "/library?skill=reading" },
        { label: "Listening", href: "/library?skill=listening" },
        { label: "Speaking", href: "/library?skill=speaking" },
        { label: "Writing", href: "/library?skill=writing" },
      ],
    },
  ],
  "/review": [
    {
      label: "Queues",
      items: [
        { label: "Grammar", href: "/review?kind=grammar" },
        { label: "Vocabulary", href: "/review?kind=vocabulary" },
      ],
    },
  ],
  "/progress": [
    {
      label: "Views",
      items: [
        { label: "Pathway", href: "/progress" },
        { label: "Skills", href: "/progress#skills" },
        { label: "History", href: "/progress#history" },
      ],
    },
  ],
};

export function ContextualRail() {
  const pathname = usePathname();
  const match = Object.keys(RAIL_BY_ROUTE).find((p) => pathname.startsWith(p));
  const sections = match ? RAIL_BY_ROUTE[match] : [];
  if (sections.length === 0) return null;
  return (
    <aside className="hidden w-56 shrink-0 border-r border-[color:var(--color-border)] px-6 py-12 text-sm md:block">
      {sections.map((section) => (
        <div key={section.label} className="mb-8">
          <p className="eyebrow mb-3">{section.label}</p>
          <ul className="flex flex-col gap-2">
            {section.items.map((item) => {
              const active = pathname + "#" === item.href || pathname === item.href;
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "true" : undefined}
                    className={`block text-[0.9rem] transition-colors duration-150 [transition-timing-function:var(--ease-out-quart)] ${
                      active
                        ? "text-[color:var(--color-ink)]"
                        : "text-[color:var(--color-ink-muted)] hover:text-[color:var(--color-ink)]"
                    }`}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </aside>
  );
}
