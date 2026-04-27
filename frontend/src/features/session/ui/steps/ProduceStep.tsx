"use client";

import { useMemo, useState } from "react";

const TARGET_MIN = 60;
const TARGET_MAX = 120;

export function ProduceStep() {
  const [text, setText] = useState("");
  const count = useMemo(
    () => (text.trim() ? text.trim().split(/\s+/).length : 0),
    [text],
  );
  const tone =
    count === 0
      ? "empty"
      : count < TARGET_MIN
        ? "short"
        : count <= TARGET_MAX
          ? "on-target"
          : "over";

  return (
    <div className="flex flex-col gap-5">
      <figure className="flex flex-col gap-2">
        <blockquote className="pullquote">
          &ldquo;Summarise the main argument of today&rsquo;s reading in
          four sentences.&rdquo;
        </blockquote>
        <figcaption className="caption">
          Use at least one instance of the past perfect from the
          Practice step.
        </figcaption>
      </figure>

      <label className="flex flex-col gap-2">
        <span className="eyebrow">Your response</span>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={8}
          placeholder="Begin with the author&rsquo;s claim, then the evidence…"
          className="w-full resize-y rounded-lg border border-[color:var(--color-border)] bg-[color:var(--color-surface)] px-4 py-3 font-display text-lg leading-relaxed text-[color:var(--color-ink)] placeholder:text-[color:var(--color-ink-faint)] focus:border-[color:var(--color-ink)] focus:outline-none"
        />
      </label>

      <div
        className="flex items-baseline justify-between gap-4"
        aria-live="polite"
      >
        <p className="caption tabular">
          <span
            className={
              tone === "on-target"
                ? "text-[color:var(--color-success)]"
                : tone === "over"
                  ? "text-[color:var(--color-warning)]"
                  : "text-[color:var(--color-ink-subtle)]"
            }
          >
            {count}
          </span>{" "}
          / {TARGET_MIN}&ndash;{TARGET_MAX} words
        </p>
        <p className="caption">
          {tone === "empty"
            ? "No pressure — begin whenever you&rsquo;re ready."
            : tone === "short"
              ? "Keep going — a little more."
              : tone === "on-target"
                ? "Within target. Stop here or tighten."
                : "Over the target — try trimming to the strongest four sentences."}
        </p>
      </div>
    </div>
  );
}
