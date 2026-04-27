import type { ReactNode } from "react";

export interface ItemRowProps {
  title: string;
  meta?: string;
  children?: ReactNode;
}

export function ItemRow({ title, meta, children }: ItemRowProps) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-[color:var(--color-border)] py-4 last:border-b-0">
      <div className="flex min-w-0 flex-col gap-1">
        <p className="truncate font-[family-name:var(--font-literata)] text-base text-[color:var(--color-ink)]">
          {title}
        </p>
        {meta ? (
          <p className="text-xs text-[color:var(--color-ink-subtle)]">{meta}</p>
        ) : null}
      </div>
      {children}
    </div>
  );
}
