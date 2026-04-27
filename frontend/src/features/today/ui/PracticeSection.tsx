export function PracticeSection({
  grammar,
  vocab,
}: {
  grammar: string;
  vocab: string[];
}) {
  return (
    <section
      aria-labelledby="practice-heading"
      className="grid gap-8 border-t border-[color:var(--color-rule)] pt-10 md:grid-cols-[1.2fr,1fr]"
    >
      <div className="flex flex-col gap-3">
        <p className="eyebrow">Practice &middot; Grammar</p>
        <h2
          id="practice-heading"
          className="font-display text-2xl font-semibold tracking-tight text-[color:var(--color-ink)]"
        >
          {grammar}
        </h2>
        <p className="text-[color:var(--color-ink-muted)]">
          Drawn directly from the passage above &mdash; noticing it in
          context is already half the work. Practice surfaces it three
          more times in the session.
        </p>
      </div>

      <div className="flex flex-col gap-3 border-l border-[color:var(--color-rule)] pl-8">
        <p className="eyebrow">Practice &middot; Vocabulary</p>
        <p className="text-[color:var(--color-ink-muted)]">
          Three words from today&rsquo;s piece, queued for your review
          deck:
        </p>
        <ul className="flex flex-wrap gap-x-5 gap-y-1 font-display text-lg text-[color:var(--color-ink)]">
          {vocab.map((word, i) => (
            <li
              key={word}
              className="after:ml-5 after:text-[color:var(--color-ink-faint)] after:content-['·'] last:after:content-none"
            >
              <span className="italic">{word}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
