export function SessionProgressBar({
  step,
  total,
}: {
  step: number;
  total: number;
}) {
  const pct = step / total;
  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={total}
      aria-valuenow={step}
      aria-label={`Session progress, step ${step} of ${total}`}
      className="h-[2px] w-full overflow-hidden bg-[color:var(--color-rule)]"
    >
      <div
        className="h-full bg-[color:var(--color-accent)] transition-[width] duration-[320ms] [transition-timing-function:var(--ease-out-expo)]"
        style={{ width: `${pct * 100}%` }}
      />
    </div>
  );
}
