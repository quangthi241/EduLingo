export function ProduceSection({ prompt }: { prompt: string }) {
  return (
    <section
      aria-labelledby="produce-heading"
      className="flex flex-col gap-5 border-t border-[color:var(--color-rule)] pt-10"
    >
      <header className="flex flex-col gap-2">
        <p className="eyebrow">Produce &middot; Short response</p>
        <h2
          id="produce-heading"
          className="font-display text-2xl font-semibold tracking-tight"
        >
          Write a short response.
        </h2>
      </header>

      <figure className="flex flex-col gap-2">
        <blockquote className="pullquote text-[color:var(--color-ink)]">
          &ldquo;{prompt}&rdquo;
        </blockquote>
        <figcaption className="caption tabular">
          Target: 60&ndash;120 words &middot; graded against the B2
          coherence rubric
        </figcaption>
      </figure>

      <div className="surface-sunken flex items-baseline justify-between gap-4 p-4 text-sm text-[color:var(--color-ink-subtle)]">
        <span>
          You&rsquo;ll draft this inside the session &mdash; no pressure,
          and no word-counter panic.
        </span>
        <span className="eyebrow">Auto-saved</span>
      </div>
    </section>
  );
}
