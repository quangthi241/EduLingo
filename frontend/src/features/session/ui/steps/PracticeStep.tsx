"use client";

import { useState } from "react";

const CHOICES = [
  { id: "a", label: "had already moved" },
  { id: "b", label: "moved" },
  { id: "c", label: "has moved" },
  { id: "d", label: "was moving" },
] as const;

const CORRECT = "a" as const;

export function PracticeStep() {
  const [selected, setSelected] = useState<string | null>(null);
  const isCorrect = selected === CORRECT;

  return (
    <div className="flex flex-col gap-6">
      <p className="caption">
        A past-perfect question pulled from today&rsquo;s reading.
      </p>

      <figure className="flex flex-col gap-3">
        <blockquote className="pullquote">
          &ldquo;By the time the municipal maps had caught up with the
          erosion at Sable Point, the coastline _______ eleven metres
          inland.&rdquo;
        </blockquote>
        <figcaption className="caption">
          Fill the blank with the form that matches the frame.
        </figcaption>
      </figure>

      <ul className="flex flex-col gap-2" role="radiogroup" aria-label="Choices">
        {CHOICES.map((c) => {
          const isSel = selected === c.id;
          const showState = selected !== null;
          const state = !showState
            ? "idle"
            : c.id === CORRECT
              ? "correct"
              : isSel
                ? "wrong"
                : "idle";
          return (
            <li key={c.id}>
              <button
                role="radio"
                aria-checked={isSel}
                onClick={() => setSelected(c.id)}
                className={`w-full rounded-lg border px-4 py-3 text-left text-[0.95rem] transition-[background-color,border-color,color] duration-150 [transition-timing-function:var(--ease-out-quart)] ${
                  state === "correct"
                    ? "border-[color:var(--color-success)] bg-[color:var(--color-success)]/10 text-[color:var(--color-ink)]"
                    : state === "wrong"
                      ? "border-[color:var(--color-danger)] bg-[color:var(--color-danger)]/10 text-[color:var(--color-ink)]"
                      : isSel
                        ? "border-[color:var(--color-ink)] bg-[color:var(--color-surface)] text-[color:var(--color-ink)]"
                        : "border-[color:var(--color-border)] bg-[color:var(--color-surface)] text-[color:var(--color-ink-muted)] hover:border-[color:var(--color-ink)] hover:text-[color:var(--color-ink)]"
                }`}
              >
                <span className="eyebrow mr-3 inline-block tabular text-[color:var(--color-ink-faint)]">
                  {c.id.toUpperCase()}
                </span>
                <span>{c.label}</span>
              </button>
            </li>
          );
        })}
      </ul>

      {selected !== null ? (
        <div
          role="status"
          className={`surface-sunken flex flex-col gap-2 p-4 ${
            isCorrect
              ? "bg-[color:var(--color-success)]/10"
              : "bg-[color:var(--color-warning)]/10"
          }`}
        >
          <p className="eyebrow">
            {isCorrect ? "That&rsquo;s it" : "Try once more"}
          </p>
          <p className="text-sm text-[color:var(--color-ink)]">
            The past perfect (<em>had moved</em>) sits beneath another
            past action (<em>the maps caught up</em>). &ldquo;By the
            time&rdquo; is the signal: one thing finished before another
            began.
          </p>
        </div>
      ) : null}
    </div>
  );
}
