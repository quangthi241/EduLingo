export interface MastheadProps {
  date: Date;
  goalLabel: string;
}

const WEEKDAY = new Intl.DateTimeFormat("en", {
  weekday: "long",
  day: "numeric",
  month: "long",
});

const ISSUE = new Intl.DateTimeFormat("en", {
  year: "numeric",
  month: "short",
});

export function Masthead({ date, goalLabel }: MastheadProps) {
  return (
    <header className="flex flex-col gap-3 border-b border-[color:var(--color-border-strong)] pb-5">
      <div className="flex items-baseline justify-between gap-4">
        <p className="dateline text-lg">{WEEKDAY.format(date)}</p>
        <span className="eyebrow tabular text-[color:var(--color-ink-muted)]">
          Vol. {ISSUE.format(date)}
        </span>
      </div>
      <div className="flex flex-wrap items-baseline gap-x-4 gap-y-2">
        <p className="eyebrow">Today&rsquo;s brief</p>
        <span
          className="inline-flex items-baseline gap-1.5 rounded-full border border-[color:var(--color-border)] px-3 py-0.5 text-xs tracking-wide"
          aria-label={`Goal: ${goalLabel}`}
        >
          <span className="text-[color:var(--color-ink-subtle)]">Toward</span>
          <span className="font-medium text-[color:var(--color-ink)]">{goalLabel}</span>
        </span>
      </div>
    </header>
  );
}
