export function ReflectionPrompt({ prompt }: { prompt: string }) {
  return (
    <aside
      aria-label="Carry-forward reflection"
      className="mt-6 flex flex-col gap-2 border-t border-[color:var(--color-border-strong)] pt-8"
    >
      <p className="eyebrow">Carry-forward</p>
      <p className="font-display text-xl italic leading-relaxed text-[color:var(--color-ink-muted)]">
        {prompt}
      </p>
      <p className="caption">
        A single question to sit with after you close this brief.
      </p>
    </aside>
  );
}
