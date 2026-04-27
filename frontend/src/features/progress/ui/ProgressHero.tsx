export function ProgressHero({ days, cefr }: { days: number; cefr: string }) {
  return (
    <section
      aria-labelledby="pathway-heading"
      className="flex flex-col gap-5 border-b border-[color:var(--color-border-strong)] pb-10"
    >
      <p className="eyebrow">Pathway</p>
      <h1
        id="pathway-heading"
        className="display-2xl text-[color:var(--color-ink)]"
      >
        <span className="tabular">{days}</span>{" "}
        <span className="text-[color:var(--color-ink-muted)]">days on pathway</span>
      </h1>
      <p className="max-w-[60ch] text-lg text-[color:var(--color-ink-muted)]">
        You&rsquo;re placed at{" "}
        <span className="font-medium text-[color:var(--color-ink)]">{cefr}</span>
        . Reading has held steady for three sessions running; listening is
        the skill moving most this week. Progress is measured honestly, in
        the work itself &mdash; not in consecutive-day counters.
      </p>
    </section>
  );
}
