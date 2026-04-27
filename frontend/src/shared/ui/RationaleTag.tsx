export interface RationaleTagProps {
  label: string;
  reason: string;
}

export function RationaleTag({ label, reason }: RationaleTagProps) {
  return (
    <p className="text-xs text-[color:var(--color-ink-subtle)]">
      <span className="font-medium text-[color:var(--color-ink-muted)]">{label}</span>
      <span className="mx-1.5">·</span>
      <span>because {reason}</span>
    </p>
  );
}
