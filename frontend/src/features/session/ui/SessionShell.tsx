"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@shared/ui/Button";
import { SessionProgressBar } from "./SessionProgressBar";
import { IntakeStep } from "./steps/IntakeStep";
import { PracticeStep } from "./steps/PracticeStep";
import { ProduceStep } from "./steps/ProduceStep";

const STEPS = [
  { id: "intake", label: "Intake", eyebrow: "One · Read" },
  { id: "practice", label: "Practice", eyebrow: "Two · Notice" },
  { id: "produce", label: "Produce", eyebrow: "Three · Respond" },
] as const;

export function SessionShell({ sessionId }: { sessionId: string }) {
  void sessionId;
  const [index, setIndex] = useState(0);
  const current = STEPS[index];
  const isLast = index === STEPS.length - 1;

  return (
    <div className="mx-auto flex max-w-[68ch] flex-col gap-10">
      <header className="flex flex-col gap-4">
        <div className="flex items-baseline justify-between gap-4">
          <Link
            href="/today"
            className="text-sm text-[color:var(--color-ink-subtle)] transition-colors hover:text-[color:var(--color-ink)]"
          >
            <span aria-hidden>&larr;</span> Exit session
          </Link>
          <span className="eyebrow tabular">
            Step {index + 1} of {STEPS.length}
          </span>
        </div>
        <SessionProgressBar step={index + 1} total={STEPS.length} />
        <StepChips index={index} />
      </header>

      <section className="flex flex-col gap-6">
        <header className="flex flex-col gap-2">
          <p className="eyebrow">{current.eyebrow}</p>
          <h1 className="display-lg text-[color:var(--color-ink)]">
            {current.label}
          </h1>
        </header>
        <StepBody id={current.id} />
      </section>

      <footer className="flex items-center justify-between gap-3 border-t border-[color:var(--color-rule)] pt-6">
        {index > 0 ? (
          <Button variant="ghost" onClick={() => setIndex((i) => i - 1)}>
            <span aria-hidden>&larr;</span> Back
          </Button>
        ) : (
          <span />
        )}
        {isLast ? (
          <Link
            href="/today"
            className="inline-flex items-center gap-2 rounded-full bg-[color:var(--color-accent)] px-5 py-2.5 text-sm font-medium text-[color:var(--color-accent-ink)] transition hover:brightness-95"
          >
            Finish session
          </Link>
        ) : (
          <Button onClick={() => setIndex((i) => i + 1)}>
            Next <span aria-hidden>&rarr;</span>
          </Button>
        )}
      </footer>
    </div>
  );
}

function StepChips({ index }: { index: number }) {
  return (
    <ol className="flex gap-3" aria-label="Session phases">
      {STEPS.map((s, i) => {
        const state = i < index ? "done" : i === index ? "active" : "upcoming";
        return (
          <li
            key={s.id}
            aria-label={s.label}
            aria-current={state === "active" ? "step" : undefined}
            className="flex items-center gap-3"
          >
            <span
              aria-hidden
              className={`eyebrow tabular ${
                state === "active"
                  ? "text-[color:var(--color-ink)]"
                  : state === "done"
                    ? "text-[color:var(--color-ink-muted)]"
                    : "text-[color:var(--color-ink-faint)]"
              }`}
            >
              {String(i + 1).padStart(2, "0")}
            </span>
            {i < STEPS.length - 1 ? (
              <span
                aria-hidden
                className={`h-px w-8 ${
                  i < index
                    ? "bg-[color:var(--color-ink-muted)]"
                    : "bg-[color:var(--color-rule)]"
                }`}
              />
            ) : null}
          </li>
        );
      })}
    </ol>
  );
}

function StepBody({ id }: { id: (typeof STEPS)[number]["id"] }) {
  if (id === "intake") return <IntakeStep />;
  if (id === "practice") return <PracticeStep />;
  return <ProduceStep />;
}
