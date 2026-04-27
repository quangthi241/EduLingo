export function SkillMeter({
  name,
  level,
  target,
  pct,
}: {
  name: string;
  level: string;
  target: string;
  pct: number;
}) {
  const atTarget = level === target;
  const percent = Math.round(pct * 100);

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-baseline justify-between gap-3">
        <span className="font-display text-lg text-[color:var(--color-ink)]">
          {name}
        </span>
        <span className="caption tabular text-[color:var(--color-ink-subtle)]">
          <span className="font-medium text-[color:var(--color-ink)]">
            {level}
          </span>
          {!atTarget ? (
            <>
              {" "}
              <span aria-hidden>&rarr;</span>{" "}
              <span className="text-[color:var(--color-ink-muted)]">{target}</span>
            </>
          ) : (
            <>
              {" "}
              <span className="text-[color:var(--color-success)]">held at target</span>
            </>
          )}
        </span>
      </div>
      <div
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percent}
        aria-label={`${name} progress toward ${target}`}
        className="relative h-1 w-full overflow-hidden bg-[color:var(--color-rule)]"
      >
        <div
          className="h-full bg-[color:var(--color-accent)] transition-[width] duration-[420ms] [transition-timing-function:var(--ease-out-expo)]"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
