"use client";

import { useState } from "react";
import { Button } from "@shared/ui/Button";

const MINUTES_CHOICES = [15, 20, 30, 45] as const;
const HINTS = [
  { id: "beginner", label: "Beginner — just starting" },
  { id: "elementary", label: "Elementary — can handle basics" },
  { id: "intermediate", label: "Intermediate — can converse" },
  { id: "advanced", label: "Advanced — refining nuance" },
] as const;

type Hint = (typeof HINTS)[number]["id"];

export interface ContextStepValue {
  minutesPerDay: number;
  startingHint: Hint;
}

export interface ContextStepProps {
  suggestedMinutes: number;
  onNext: (value: ContextStepValue) => void;
}

export function ContextStep({ suggestedMinutes, onNext }: ContextStepProps) {
  const [minutes, setMinutes] = useState<number>(suggestedMinutes);
  const [hint, setHint] = useState<Hint>("intermediate");

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          Step 2 of 3
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-3xl font-semibold tracking-tight">
          Your rhythm.
        </h1>
      </header>

      <fieldset className="flex flex-col gap-3">
        <legend className="text-sm font-medium text-[color:var(--color-ink-muted)]">
          Minutes per day
        </legend>
        <div className="flex flex-wrap gap-2">
          {MINUTES_CHOICES.map((m) => (
            <label
              key={m}
              className={`cursor-pointer rounded-full border px-4 py-2 text-sm transition ${
                minutes === m
                  ? "border-[color:var(--color-accent)] bg-[color:var(--color-accent)] text-[color:var(--color-accent-ink)]"
                  : "border-[color:var(--color-border)]"
              }`}
            >
              <input
                type="radio"
                name="minutes"
                value={m}
                checked={minutes === m}
                onChange={() => setMinutes(m)}
                className="sr-only"
              />
              {m}
            </label>
          ))}
        </div>
      </fieldset>

      <fieldset className="flex flex-col gap-3">
        <legend className="text-sm font-medium text-[color:var(--color-ink-muted)]">
          Roughly where you are now
        </legend>
        <div className="flex flex-col gap-2">
          {HINTS.map((h) => (
            <label
              key={h.id}
              className={`cursor-pointer rounded-lg border p-4 transition ${
                hint === h.id
                  ? "border-[color:var(--color-accent)]"
                  : "border-[color:var(--color-border)]"
              }`}
            >
              <input
                type="radio"
                name="hint"
                value={h.id}
                checked={hint === h.id}
                onChange={() => setHint(h.id)}
                className="sr-only"
              />
              {h.label}
            </label>
          ))}
        </div>
      </fieldset>

      <Button onClick={() => onNext({ minutesPerDay: minutes, startingHint: hint })}>
        Continue
      </Button>
    </div>
  );
}
