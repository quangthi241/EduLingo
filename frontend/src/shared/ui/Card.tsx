import type { ReactNode } from "react";

export function Card({
  children,
  className = "",
  as: Tag = "div",
}: {
  children: ReactNode;
  className?: string;
  as?: "div" | "article" | "section";
}) {
  return (
    <Tag className={`surface-card p-6 ${className}`}>{children}</Tag>
  );
}

export interface SectionProps {
  eyebrow?: string;
  heading: string;
  lede?: string;
  children: ReactNode;
  id?: string;
  /** Visual treatment. "heading" is default; "ruled" draws a thin top rule. */
  variant?: "heading" | "ruled";
  /** Heading typographic size. */
  size?: "md" | "lg";
}

export function Section({
  eyebrow,
  heading,
  lede,
  children,
  id,
  variant = "heading",
  size = "md",
}: SectionProps) {
  const headingClass =
    size === "lg"
      ? "display-lg"
      : "font-display text-2xl font-semibold tracking-tight";
  return (
    <section id={id} className="flex flex-col gap-4">
      {variant === "ruled" ? <hr className="rule" aria-hidden /> : null}
      <header className="flex flex-col gap-2">
        {eyebrow ? <span className="eyebrow">{eyebrow}</span> : null}
        <h2 className={headingClass}>{heading}</h2>
        {lede ? (
          <p className="max-w-[60ch] text-[color:var(--color-ink-muted)]">
            {lede}
          </p>
        ) : null}
      </header>
      {children}
    </section>
  );
}
