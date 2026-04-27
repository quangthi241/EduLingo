import Link from "next/link";

export function IntakeSection({
  title,
  minutes,
  cefr,
}: {
  title: string;
  minutes: number;
  cefr: string;
}) {
  return (
    <section aria-labelledby="intake-heading" className="flex flex-col gap-5">
      <header className="flex flex-col gap-3">
        <div className="flex items-baseline justify-between gap-4">
          <span className="eyebrow">Intake &middot; Reading</span>
          <span className="caption tabular">
            {minutes} min &middot; {cefr}
          </span>
        </div>
        <h2
          id="intake-heading"
          className="display-lg text-[color:var(--color-ink)]"
        >
          {title}
        </h2>
      </header>

      <figure className="flex flex-col gap-3">
        <blockquote className="pullquote border-l-0 pl-0 text-[color:var(--color-ink)]">
          &ldquo;The shoreline looks firm from a distance, but it is in constant
          negotiation with the sea &mdash; a slow, decisive erosion the maps
          will catch up to only years from now.&rdquo;
        </blockquote>
        <figcaption className="caption">
          An excerpt from the opening paragraph.
        </figcaption>
      </figure>

      <p className="text-[color:var(--color-ink-muted)]">
        Read at your own pace. Click any word for a gloss; the passage is
        paired with today&rsquo;s grammar and vocabulary below.
      </p>

      <div className="flex flex-wrap items-center gap-3 pt-1">
        <Link
          href="/session/today-intake"
          className="inline-flex items-center rounded-full bg-[color:var(--color-accent)] px-5 py-2.5 text-sm font-medium text-[color:var(--color-accent-ink)] transition hover:brightness-95"
        >
          Start reading
        </Link>
        <span className="caption">or skim the highlights first &mdash;</span>
        <Link
          href="/library"
          className="text-sm text-[color:var(--color-ink-muted)] underline-offset-4 hover:text-[color:var(--color-ink)] hover:underline"
        >
          browse library
        </Link>
      </div>
    </section>
  );
}
