"use client";

import { GOAL_PRESETS, type GoalPreset } from "../domain/presets";

export interface GoalPickerProps {
  onSelect: (id: GoalPreset["id"]) => void;
}

export function GoalPicker({ onSelect }: GoalPickerProps) {
  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          Step 1 of 3
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-3xl font-semibold tracking-tight">
          What are you studying for?
        </h1>
        <p className="text-[color:var(--color-ink-muted)]">
          Pick the outcome that matters most. You can adjust later.
        </p>
      </header>
      <ul className="flex flex-col gap-3">
        {GOAL_PRESETS.map((preset) => (
          <li key={preset.id}>
            <button
              type="button"
              onClick={() => onSelect(preset.id)}
              className="w-full rounded-lg border border-[color:var(--color-border)] bg-[color:var(--color-surface)] p-5 text-left transition hover:border-[color:var(--color-accent)]"
            >
              <p className="font-[family-name:var(--font-literata)] text-lg font-semibold">
                {preset.label}
              </p>
              <p className="mt-1 text-sm text-[color:var(--color-ink-muted)]">
                {preset.blurb}
              </p>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
