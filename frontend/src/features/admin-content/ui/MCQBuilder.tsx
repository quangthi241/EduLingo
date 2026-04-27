"use client";

import { Button } from "@shared/ui/Button";
import { Field, Label, Input } from "@shared/ui/Field";
import { Textarea } from "@shared/ui/Textarea";
import type { MCQ } from "@features/library/domain/pieces";

type Props = { value: MCQ[]; onChange: (next: MCQ[]) => void };

function emptyMCQ(): MCQ {
  return { question: "", choices: ["", ""], correctIndex: 0, rationale: "" };
}

export function MCQBuilder({ value, onChange }: Props) {
  const canRemove = value.length > 3;
  const canAdd = value.length < 5;

  function update(i: number, patch: Partial<MCQ>) {
    onChange(value.map((q, idx) => (idx === i ? { ...q, ...patch } : q)));
  }

  function updateChoice(i: number, ci: number, text: string) {
    const choices = [...value[i].choices];
    choices[ci] = text;
    update(i, { choices });
  }

  function addChoice(i: number) {
    if (value[i].choices.length >= 5) return;
    update(i, { choices: [...value[i].choices, ""] });
  }

  function removeChoice(i: number, ci: number) {
    if (value[i].choices.length <= 2) return;
    const choices = value[i].choices.filter((_, x) => x !== ci);
    const correctIndex = Math.min(value[i].correctIndex, choices.length - 1);
    update(i, { choices, correctIndex });
  }

  return (
    <div className="flex flex-col gap-4">
      {value.map((q, i) => (
        <fieldset key={i} className="rounded-xl border border-border p-4 flex flex-col gap-3">
          <legend className="px-1 text-sm text-ink-muted">Question {i + 1}</legend>
          <Field>
            <Label htmlFor={`q-${i}`}>Question {i + 1}</Label>
            <Input
              id={`q-${i}`}
              value={q.question}
              onChange={(e) => update(i, { question: e.target.value })}
            />
          </Field>
          <div className="flex flex-col gap-2">
            {q.choices.map((c, ci) => (
              <div key={ci} className="flex items-center gap-2">
                <input
                  type="radio"
                  name={`correct-${i}`}
                  checked={q.correctIndex === ci}
                  onChange={() => update(i, { correctIndex: ci })}
                  aria-label={`Mark choice ${ci + 1} correct`}
                />
                <Input
                  id={`q-${i}-c-${ci}`}
                  value={c}
                  onChange={(e) => updateChoice(i, ci, e.target.value)}
                  placeholder={`Choice ${ci + 1}`}
                />
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => removeChoice(i, ci)}
                  disabled={q.choices.length <= 2}
                  aria-label={`Remove choice ${ci + 1}`}
                >
                  −
                </Button>
              </div>
            ))}
            <Button
              type="button"
              variant="ghost"
              onClick={() => addChoice(i)}
              disabled={q.choices.length >= 5}
            >
              + Add choice
            </Button>
          </div>
          <Textarea
            label="Rationale"
            id={`rationale-${i}`}
            value={q.rationale}
            onChange={(e) => update(i, { rationale: e.target.value })}
            rows={2}
          />
          <div className="flex justify-end">
            <Button
              type="button"
              variant="ghost"
              onClick={() => onChange(value.filter((_, x) => x !== i))}
              disabled={!canRemove}
              aria-label={`Remove question ${i + 1}`}
            >
              Remove question
            </Button>
          </div>
        </fieldset>
      ))}
      <Button type="button" onClick={() => onChange([...value, emptyMCQ()])} disabled={!canAdd}>
        Add question
      </Button>
    </div>
  );
}
