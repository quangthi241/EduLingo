"use client";

import { Button } from "@shared/ui/Button";

export function PlacementIntro({ onBegin }: { onBegin: () => void }) {
  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          Step 3 of 3
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-3xl font-semibold tracking-tight">
          A short placement.
        </h1>
      </header>
      <p className="max-w-[60ch] text-[color:var(--color-ink-muted)]">
        We&apos;ll adapt as you go, so you won&apos;t see questions that are far too easy
        or too hard. It takes about 10 minutes and sets your pathway. You can
        pause and resume.
      </p>
      <Button onClick={onBegin}>Begin placement</Button>
    </div>
  );
}
