"use client";

import { useState } from "react";
import type { ReviewItem } from "../domain/queue";

type Rating = "again" | "hard" | "good" | "easy";

const RATINGS: { id: Rating; label: string; tone: string }[] = [
  {
    id: "again",
    label: "Again",
    tone: "border-[color:var(--color-danger)] text-[color:var(--color-danger)] hover:bg-[color:var(--color-danger)]/10",
  },
  {
    id: "hard",
    label: "Hard",
    tone: "border-[color:var(--color-warning)] text-[color:var(--color-warning)] hover:bg-[color:var(--color-warning)]/10",
  },
  {
    id: "good",
    label: "Good",
    tone: "border-[color:var(--color-success)] text-[color:var(--color-success)] hover:bg-[color:var(--color-success)]/10",
  },
  {
    id: "easy",
    label: "Easy",
    tone: "border-[color:var(--color-ink)] text-[color:var(--color-ink)] hover:bg-[color:var(--color-surface-sunken)]",
  },
];

export function ReviewCard({
  item,
  position,
  total,
  onRate,
}: {
  item: ReviewItem;
  position: number;
  total: number;
  onRate: (rating: Rating) => void;
}) {
  const [revealed, setRevealed] = useState(false);

  return (
    <section
      aria-labelledby="review-card"
      className="flex flex-col gap-6"
    >
      <div className="surface-card relative flex min-h-[22rem] flex-col gap-5 p-8 md:p-10">
        <div className="flex items-baseline justify-between gap-3">
          <span className="eyebrow">Recall</span>
          <span className="eyebrow tabular text-[color:var(--color-ink-muted)]">
            {position} of {total}
          </span>
        </div>

        <div className="flex flex-1 flex-col justify-center gap-6 py-4">
          <p
            id="review-card"
            className="display-lg text-[color:var(--color-ink)]"
          >
            {item.cue}
          </p>

          {revealed ? (
            <div className="flex flex-col gap-3">
              <p className="prose-editorial text-base text-[color:var(--color-ink)]">
                {item.answer}
              </p>
              {item.example ? (
                <figure>
                  <blockquote className="pullquote text-lg text-[color:var(--color-ink-muted)]">
                    &ldquo;{item.example}&rdquo;
                  </blockquote>
                </figure>
              ) : null}
            </div>
          ) : null}
        </div>

        {!revealed ? (
          <button
            onClick={() => setRevealed(true)}
            className="rounded-full border border-[color:var(--color-border-strong)] bg-transparent px-5 py-2.5 text-sm font-medium text-[color:var(--color-ink)] transition hover:border-[color:var(--color-ink)] hover:bg-[color:var(--color-surface-sunken)]"
          >
            Reveal answer &middot; <span className="text-[color:var(--color-ink-subtle)]">space</span>
          </button>
        ) : (
          <div className="grid grid-cols-2 gap-2 md:grid-cols-4" aria-label="Rate recall">
            {RATINGS.map((r) => (
              <button
                key={r.id}
                onClick={() => onRate(r.id)}
                className={`rounded-full border bg-transparent px-3 py-2.5 text-sm font-medium transition-[background-color,border-color,transform] duration-150 [transition-timing-function:var(--ease-out-quart)] active:translate-y-[0.5px] ${r.tone}`}
              >
                {r.label}
              </button>
            ))}
          </div>
        )}
      </div>

      <p className="caption">
        {revealed
          ? "Rate honestly &mdash; the interval to next review depends on it."
          : "Try to recall before revealing. It feels uncomfortable; that&rsquo;s the work."}
      </p>
    </section>
  );
}
